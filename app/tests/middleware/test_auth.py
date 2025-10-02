import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from api_v1.auth.token_auth import AuthService
from api_v1.users.schemas import UserPublic
from core.config import settings


class TestAuthService:
    @pytest.fixture
    def auth_service(self):
        return AuthService()

    @pytest.fixture
    def sample_user(self):
        return UserPublic(
            id=1, login="testuser", name="Test User", email="test@example.com"
        )

    def test_initialization(self):
        """Test that AuthService initializes correctly"""
        service = AuthService()

        assert hasattr(service, "token_director")
        assert service.token_director is not None
        assert service.create_jwt is not None

    def test_create_jwt(self, auth_service):
        """Test JWT creation with payload"""
        token_data = {"sub": 1, "login": "testuser"}
        token_type = "access"

        with patch.object(auth_service, "encode_jwt") as mock_encode:
            mock_encode.return_value = "encoded.jwt"

            result = auth_service.create_jwt(
                token_type=token_type, token_data=token_data, expire_minutes=30
            )

            expected_payload = {"type": token_type, **token_data}
            mock_encode.assert_called_once_with(
                expected_payload, expire_minutes=30, expire_timedelta=None
            )
            assert result == "encoded.jwt"

    def test_create_jwt_with_timedelta(self, auth_service):
        """Test JWT creation with timedelta expiration"""
        token_data = {"sub": 1, "login": "testuser"}
        expire_timedelta = timedelta(days=7)

        with patch.object(auth_service, "encode_jwt") as mock_encode:
            mock_encode.return_value = "encoded.jwt"

            result = auth_service.create_jwt(
                token_type="refresh",
                token_data=token_data,
                expire_timedelta=expire_timedelta,
            )

            mock_encode.assert_called_once_with(
                {"type": "refresh", **token_data},
                expire_minutes=None,
                expire_timedelta=expire_timedelta,
            )

    @patch("api_v1.auth.token_auth.datetime")
    @patch("api_v1.auth.token_auth.jwt.encode")
    def test_encode_jwt_with_minutes(
        self, mock_jwt_encode, mock_datetime, auth_service
    ):
        """Test JWT encoding with minutes expiration"""

        fixed_now = datetime(2025, 12, 2, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now

        with patch("pathlib.Path.read_text") as mock_read:
            mock_read.return_value = "fake_private_key"

            mock_jwt_encode.return_value = "encoded.token"

            payload = {"sub": 1, "login": "testuser"}
            result = auth_service.encode_jwt(payload, expire_minutes=30)

            expected_expire = fixed_now + timedelta(minutes=30)

            mock_jwt_encode.assert_called_once()
            call_args = mock_jwt_encode.call_args[0]
            call_kwargs = mock_jwt_encode.call_args[1]

            encoded_payload = call_args[0]
            assert encoded_payload["sub"] == 1
            assert encoded_payload["login"] == "testuser"
            assert encoded_payload["exp"] == expected_expire
            assert encoded_payload["iat"] == fixed_now

            assert call_kwargs["algorithm"] == settings.auth_jwt.algorithm

            mock_read.assert_called_once()

            assert result == "encoded.token"

    @patch("api_v1.auth.token_auth.datetime")
    @patch("api_v1.auth.token_auth.jwt.encode")
    def test_encode_jwt_with_timedelta(
        self, mock_jwt_encode, mock_datetime, auth_service
    ):
        """Test JWT encoding with timedelta expiration"""
        fixed_now = datetime(2025, 12, 2, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now

        with patch("pathlib.Path.read_text") as mock_read:
            mock_read.return_value = "fake_private_key"

            mock_jwt_encode.return_value = "encoded.token"

            payload = {"sub": 1}
            expire_timedelta = timedelta(days=7)
            result = auth_service.encode_jwt(payload, expire_timedelta=expire_timedelta)

            expected_expire = fixed_now + expire_timedelta

            encoded_payload = mock_jwt_encode.call_args[0][0]
            assert encoded_payload["exp"] == expected_expire

    @patch("api_v1.auth.token_auth.datetime")
    @patch("api_v1.auth.token_auth.jwt.encode")
    def test_encode_jwt_default_expiration(
        self, mock_jwt_encode, mock_datetime, auth_service
    ):
        """Test JWT encoding with default expiration"""
        fixed_now = datetime(2025, 12, 2, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now

        with patch("pathlib.Path.read_text") as mock_read:
            mock_read.return_value = "fake_private_key"

            auth_service.encode_jwt({"sub": 1})

            expected_expire = fixed_now + timedelta(
                minutes=settings.auth_jwt.access_token_expire_minutes
            )

            encoded_payload = mock_jwt_encode.call_args[0][0]
            assert encoded_payload["exp"] == expected_expire

    def test_create_access_token(self, auth_service, sample_user):
        """Test access token creation through service"""
        with patch.object(
            auth_service.token_director, "create_access_token"
        ) as mock_create:
            mock_create.return_value = "access.token"

            result = auth_service.create_access_token(sample_user)

            mock_create.assert_called_once_with(sample_user)
            assert result == "access.token"

    def test_create_refresh_token(self, auth_service, sample_user):
        """Test refresh token creation through service"""
        with patch.object(
            auth_service.token_director, "create_refresh_token"
        ) as mock_create:
            mock_create.return_value = "refresh.token"

            result = auth_service.create_refresh_token(sample_user)

            mock_create.assert_called_once_with(sample_user)
            assert result == "refresh.token"

    def test_singleton_instance(self):
        """Test that auth_service is a singleton instance"""
        from api_v1.auth.token_auth import auth_service

        from api_v1.auth.token_auth import auth_service as auth_service2

        assert auth_service is auth_service2

    def test_encode_jwt_handles_jwt_exception(self, auth_service):
        """Test that encode_jwt properly handles JWT encoding exceptions"""
        with patch("pathlib.Path.read_text") as mock_read:
            mock_read.return_value = "fake_private_key"

            with patch("api_v1.auth.token_auth.jwt.encode") as mock_jwt_encode:
                mock_jwt_encode.side_effect = Exception("JWT encoding failed")

                with pytest.raises(Exception, match="JWT encoding failed"):
                    auth_service.encode_jwt({"sub": 1})

    def test_encode_jwt_with_custom_private_key_path(self, auth_service):
        """Test JWT encoding with custom private key path handling"""
        with patch("pathlib.Path.read_text") as mock_read:
            mock_read.return_value = "custom_private_key"

            with patch("api_v1.auth.token_auth.jwt.encode") as mock_jwt_encode:
                mock_jwt_encode.return_value = "encoded.token"

                auth_service.encode_jwt({"sub": 1})

                mock_read.assert_called_once()
