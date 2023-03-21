import sys

from ..app_utils import safe_get_env_var, NotFoundError, AlreadyExistsError
ael_python_path = safe_get_env_var("FA_AEL_PYTHON_PATH")
sys.path.append(ael_python_path)


class FAUserHelper:
    @classmethod
    def _get_current_fa_user(cls, user_id):
        import acm
        fa_user = acm.FUser[user_id]
        if not fa_user:
            raise NotFoundError(f"Front Arena user with user id {user_id} not found")
        return fa_user

    @classmethod
    def _get_fa_group(cls, user_id):
        import acm
        fa_user = acm.FUser[user_id]
        if not fa_user:
            raise NotFoundError(f"Front Arena user with user id {user_id} not found")
        return fa_user

    @classmethod
    def activate_user(cls, user_id):
        user = cls._get_current_fa_user(user_id)
        user_image = user.StorageImage()
        user_image.Active(True)
        user_image.Commit()
        return user_image

    @classmethod
    def reset_password(cls, user_id, password):
        user = cls._get_current_fa_user(user_id)
        user_image = user.StorageImage()
        user_image.Password(password)
        user_image.Commit()
        return user_image

    @classmethod
    def assign_user_to_group(cls, user_id, group_name):
        user = cls._get_current_fa_user(user_id)
        group = acm.FUserGroup[group_name]

        user_image = user.StorageImage()
        user_image.UserGroup(group)
        user_image.Commit()
        return user_image

    @classmethod
    def remove_user_from_group(cls, user_id, group_name):
        cls.assign_user_to_group(user_id, group_name)

    @classmethod
    def create_new_user(cls, data):
        """
        data = {
            "Name": 'UserId',
            "Fullname": 'Full name',
            "Email": 'Email Address',
            "Password": 'Some Password',
        }
        :param data:
        :return:
        """
        user_id = data['Name']
        user = cls._get_current_fa_user(user_id)
        if user:
            raise AlreadyExistsError(f"Front Arena user with user id {user_id} already exist")

        user = acm.User()
        user = user(**data)
        user.Commit()

    @classmethod
    def update_user(cls, data):
        """
        data = {
            "Name": 'some*pass*word',
            "Fullname": 'some*pass*word',
            "Email": 'some*pass*word',
            "Password": 'some*pass*word',
        }
        :param data:
        :return:
        """
        user_id = data['Name']
        user = cls._get_current_fa_user(user_id)
        if not user:
            raise NotFoundError(f"Front Arena user with user id {user_id} not found")

        user = user(**data)
        user.Commit()

    @classmethod
    def get_groups(cls):
        import acm
        groups = acm.FGroup.Select('')
        return [group.Name() for group in groups]