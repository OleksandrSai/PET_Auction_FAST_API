import pytest
from datetime import timedelta
from unittest.mock import Mock, patch
from api_v1.auth.token_director import TokenDirector
from utils.enums import TokenType
from api_v1.users.schema import UserPublic
from core.config import settings


class TestTokenDirector:
    @pytest.fixture
    def mock_jwt_creator(self):
        return Mock(return_value="mock.jwt.token")

    @pytest.fixture
    def sample_user(self):
        return UserPublic(
            id=1, login="testuser", name="Test User", email="test@example.com"
        )

    @pytest.fixture
    def director(self, mock_jwt_creator):
        return TokenDirector(mock_jwt_creator)

    def test_initialization(self, mock_jwt_creator):
        """Test that TokenDirector initializes correctly"""
        director = TokenDirector(mock_jwt_creator)

        assert director._jwt_creator == mock_jwt_creator

    def test_create_access_token(self, director, mock_jwt_creator, sample_user):
        """Test access token creation with correct parameters"""
        with patch("api_v1.auth.token_director.TokenBuilder") as MockBuilder:
            mock_builder_instance = Mock()
            mock_builder_instance.for_user.return_value = mock_builder_instance
            mock_builder_instance.with_type.return_value = mock_builder_instance
            mock_builder_instance.with_expire_minutes.return_value = (
                mock_builder_instance
            )
            mock_builder_instance.build.return_value = "access.token"

            MockBuilder.return_value = mock_builder_instance

            token = director.create_access_token(sample_user)

            MockBuilder.assert_called_once_with(mock_jwt_creator)

            # Verify method chaining
            mock_builder_instance.for_user.assert_called_once_with(sample_user)
            mock_builder_instance.with_type.assert_called_once_with(TokenType.ACCESS)
            mock_builder_instance.with_expire_minutes.assert_called_once_with(
                settings.auth_jwt.access_token_expire_minutes
            )
            mock_builder_instance.build.assert_called_once()

            assert token == "access.token"

    def test_create_refresh_token(self, director, mock_jwt_creator, sample_user):
        """Test refresh token creation with correct parameters"""
        with patch("api_v1.auth.token_director.TokenBuilder") as MockBuilder:
            mock_builder_instance = Mock()
            mock_builder_instance.for_user.return_value = mock_builder_instance
            mock_builder_instance.with_type.return_value = mock_builder_instance
            mock_builder_instance.with_expire_days.return_value = mock_builder_instance
            mock_builder_instance.build.return_value = "refresh.token"

            MockBuilder.return_value = mock_builder_instance

            token = director.create_refresh_token(sample_user)

            MockBuilder.assert_called_once_with(mock_jwt_creator)

            mock_builder_instance.for_user.assert_called_once_with(sample_user)
            mock_builder_instance.with_type.assert_called_once_with(TokenType.REFRESH)
            mock_builder_instance.with_expire_days.assert_called_once_with(
                settings.auth_jwt.refresh_token_expire_days
            )
            mock_builder_instance.build.assert_called_once()

            assert token == "refresh.token"

    def test_integration_with_real_builder(self, sample_user):
        """Test integration with actual TokenBuilder (not mocked)"""

        def simple_jwt_creator(
            token_type,
            token_data,
            expire_minutes=None,
            expire_timedelta=None,
        ):
            return f"{token_type}.{token_data['sub']}.{token_data['login']}"

        director_with_real_creator = TokenDirector(simple_jwt_creator)

        access_token = director_with_real_creator.create_access_token(sample_user)

        assert (
            f"{TokenType.ACCESS}.{sample_user.id}.{sample_user.login}" in access_token
        )

    def test_integration_with_real_builder_refresh_token(self, sample_user):
        """Test integration with actual TokenBuilder for refresh token"""

        def simple_jwt_creator(
            token_type,
            token_data,
            expire_minutes=None,
            expire_timedelta=None,
        ):
            return f"{token_type}.{token_data['sub']}.{token_data['login']}"

        director = TokenDirector(simple_jwt_creator)

        refresh_token = director.create_refresh_token(sample_user)

        assert (
            f"{TokenType.REFRESH}.{sample_user.id}.{sample_user.login}" in refresh_token
        )

    def test_integration_verify_expiration_parameters(self, sample_user):
        """Test that expiration parameters are correctly passed through the chain"""
        captured_params = {}

        def capturing_jwt_creator(
            token_type, token_data, expire_minutes=None, expire_timedelta=None
        ):
            captured_params.update(
                {
                    "token_type": token_type,
                    "token_data": token_data,
                    "expire_minutes": expire_minutes,
                    "expire_timedelta": expire_timedelta,
                }
            )
            return "test.token"

        director = TokenDirector(capturing_jwt_creator)

        access_token = director.create_access_token(sample_user)

        assert captured_params["token_type"] == TokenType.ACCESS
        assert (
            captured_params["expire_minutes"]
            == settings.auth_jwt.access_token_expire_minutes
        )
        assert captured_params["expire_timedelta"] is None
        assert captured_params["token_data"]["username"] == sample_user.name

        captured_params.clear()

        refresh_token = director.create_refresh_token(sample_user)

        assert captured_params["token_type"] == TokenType.REFRESH
        assert captured_params["expire_minutes"] is None
        assert captured_params["expire_timedelta"] == timedelta(
            days=settings.auth_jwt.refresh_token_expire_days
        )
        assert "username" not in captured_params["token_data"]
