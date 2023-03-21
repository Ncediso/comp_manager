import sys
import logging

from ..app_utils import NotFoundError, AlreadyExistsError, safe_get_env_var

ael_python_path = safe_get_env_var("FA_AEL_PYTHON_PATH")
sys.path.append(ael_python_path)

LOGGER = logging.getLogger(__name__)

class FAProfilesHelper:

    @classmethod
    def get_all_profiles(cls):

        import acm
        profiles = acm.FUserProfile.Select('')
        return [profile.Name() for profile in profiles]

    @classmethod
    def get_users_profiles(cls, user_id):

        import acm
        user = acm.FUser[user_id]
        if not user:
            raise NotFoundError(f"No user found with name or id {user_id}")
        group_profile_links = acm.FUserProfileLink.Select(f"user='{user_id}'")
        profile_names = [link.UserProfile().Name() for link in group_profile_links]
        return profile_names

    @classmethod
    def get_group_profiles(cls, group_name):

        import acm
        group = acm.FUserGroup[group_name]
        if not group:
            raise NotFoundError(f"No group found with name {group_name}")
        group_profile_links = acm.FGroupProfileLink.Select(f"userGroup='{group_name}'")
        profile_names = [link.UserProfile().Name() for link in group_profile_links]
        return profile_names

    @classmethod
    def get_user_profile_links(cls, fa_user):
        user_profile_links = [link.UserProfile().Name() for link in fa_user.Links()]
        return user_profile_links

    @classmethod
    def remove_user_profile(cls, user_id, profile_name):
        import acm

        fa_user = acm.FUser[user_id]
        if not fa_user:
            raise NotFoundError(f"No user found with name or id {user_id}")

        user_profile = acm.FUserProfile[profile_name]
        if not user_profile:
            raise NotFoundError(f"Front Arena User Profile with name {profile_name} not found")

        select_str = f"groupProfile='{profile_name}' and user='{user_id}'"
        profile_link = acm.FUserProfileLink.Select(select_str)
        if not profile_link:
            raise NotFoundError(f"Front Arena Profile with name {profile_name} linked to User {user_id} not found")

        profile_link.Delete()
        LOGGER.info(f"Successfully removed User Profile {profile_name} from User {user_id}")

    @classmethod
    def remove_group_profile(cls, group_name, profile_name):
        import acm
        fa_group = acm.FUserGroup[group_name]
        if not fa_group:
            raise NotFoundError(f"No group found with name {group_name}")

        group_profile = acm.FUserProfile[profile_name]
        if not group_profile:
            raise NotFoundError(f"Front Arena Profile with name {profile_name} not found")

        select_str = f"groupProfile='{profile_name}' and userGroup='{group_name}'"
        profile_link = acm.FGroupProfileLink.Select(select_str)
        if not profile_link:
            raise NotFoundError(f"Front Arena Profile with name {profile_name} linked to Group {group_name} not found")

        profile_link.Delete()
        LOGGER.info(f"Successfully removed User Profile {profile_name} from Group {group_name}")

    @classmethod
    def assign_user_profile(cls, user_id, profile_name):
        import acm

        fa_user = acm.FUser[user_id]
        if not fa_user:
            raise NotFoundError(f"No user found with name or id {user_id}")

        user_profile = acm.FUserProfile[profile_name]
        if not user_profile:
            raise NotFoundError(f"Front Arena User Profile with name {profile_name} not found")

        select_str = f"groupProfile='{profile_name}' and user='{user_id}'"
        profile_link = acm.FUserProfileLink.Select(select_str)
        if profile_link:
            raise AlreadyExistsError(f"Front Arena User Profile with name {profile_name} already exist")

        user_profile_link = acm.FUserProfileLink()
        user_profile_link.User(fa_user)
        user_profile_link.UserProfile(user_profile)
        user_profile_link.Commit()
        LOGGER.info(f"Successfully assigned User Profile {profile_name} to User {user_id}")

    @classmethod
    def assign_group_profile(cls, group_name, profile_name):
        import acm
        fa_group = acm.FUserGroup[group_name]
        if not fa_group:
            raise NotFoundError(f"No group found with name {group_name}")

        group_profile = acm.FUserProfile[profile_name]
        if not group_profile:
            raise NotFoundError(f"Front Arena Profile with name {profile_name} not found")

        select_str = f"groupProfile='{profile_name}' and userGroup='{group_name}'"
        profile_link = acm.FGroupProfileLink.Select(select_str)
        if profile_link:
            raise AlreadyExistsError(f"Front Arena Group Profile with name {profile_name} already exist")

        group_profile_link = acm.FGroupProfileLink()
        group_profile_link.UserGroup(fa_group)
        group_profile_link.UserProfile(group_profile)
        group_profile_link.Commit()
        LOGGER.info(f"Successfully assigned User Profile {profile_name} to Group {group_name}")

