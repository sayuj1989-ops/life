#!/usr/bin/env python3
"""
Create a RAGFlow user directly via the database/API
"""

import sys

sys.path.insert(0, "/ragflow")

from api.db.services.user_service import UserService, TenantService, UserTenantService
from api.db.services.file_service import FileService
from api.db.services.tenant_llm_service import TenantLLMService
from api.db.services.llm_service import get_init_tenant_llm
from api.db import FileType, UserTenantRole
from common.misc_utils import get_uuid
from common.time_utils import get_format_time
from common import settings

# Initialize settings if needed
if hasattr(settings, "init_settings"):
    settings.init_settings()


def create_user(email, nickname, password):
    """Create a RAGFlow user"""
    user_id = get_uuid()

    user_dict = {
        "id": user_id,
        "access_token": get_uuid(),
        "email": email,
        "nickname": nickname,
        "password": password,  # Plain password, will be hashed by UserService
        "login_channel": "password",
        "last_login_time": get_format_time(),
        "is_superuser": False,
    }

    tenant = {
        "id": user_id,
        "name": nickname + "'s Kingdom",
        "llm_id": settings.CHAT_MDL,
        "embd_id": settings.EMBEDDING_MDL,
        "asr_id": settings.ASR_MDL,
        "parser_ids": settings.PARSERS,
        "img2txt_id": settings.IMAGE2TEXT_MDL,
        "rerank_id": settings.RERANK_MDL,
    }

    usr_tenant = {
        "tenant_id": user_id,
        "user_id": user_id,
        "invited_by": user_id,
        "role": UserTenantRole.OWNER,
    }

    file_id = get_uuid()
    file = {
        "id": file_id,
        "parent_id": file_id,
        "tenant_id": user_id,
        "created_by": user_id,
        "name": "/",
        "type": FileType.FOLDER.value,
        "size": 0,
        "location": "",
    }

    try:
        tenant_llm = get_init_tenant_llm(user_id)
    except Exception as e:
        print(f"Warning: Could not initialize tenant LLMs: {e}")
        tenant_llm = []

    try:
        # Check if user already exists
        existing = UserService.query(email=email)
        if existing:
            print(f"User {email} already exists!")
            return False

        # Create user and related entities
        if not UserService.save(**user_dict):
            print("Failed to save user")
            return False

        TenantService.insert(**tenant)
        UserTenantService.insert(**usr_tenant)
        TenantLLMService.insert_many(tenant_llm)
        FileService.insert(file)

        print(f"✅ Successfully created user: {email}")
        print(f"   Nickname: {nickname}")
        print(f"   Password: {password}")
        print(f"   User ID: {user_id}")
        return True

    except Exception as e:
        print(f"❌ Error creating user: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Create a default user
    email = "researcher@ragflow.local"
    nickname = "researcher"
    password = "ragflow123"

    print("Creating RAGFlow user...")
    print(f"Email: {email}")
    print(f"Nickname: {nickname}")
    print(f"Password: {password}")
    print()

    success = create_user(email, nickname, password)

    if success:
        print()
        print("=" * 60)
        print("User created successfully!")
        print("You can now login at http://localhost with:")
        print(f"  Email: {email}")
        print(f"  Password: {password}")
        print("=" * 60)
    else:
        print()
        print("Failed to create user. Check the error messages above.")
