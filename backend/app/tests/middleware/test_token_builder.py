import pytest
from datetime import timedelta
from unittest.mock import Mock, patch

from api_v1.auth.token_builder import TokenBuilder
from utils.enums import TokenType
from api_v1.users.schema import UserPublic


class TestTokenBuilder:
    @pytest.fixture
    def mock_jwt_creator(self):
        return Mock(return_value="mock.jwt.token")

    @pytest.fixture
    def sample_user(self):
        return UserPublic(
            id=1, login="testuser", name="Test User", email="test@example.com"
        )

    def test_initialization(self, mock_jwt_creator):
        """Test that TokenBuilder initializes correctly"""
        builder = TokenBuilder(mock_jwt_creator)

        assert builder._jwt_creator == mock_jwt_creator
        assert builder._token_type is None
        assert builder._user is None
        assert builder._expire_minutes is None
        assert builder._expire_timedelta is None

    def test_for_user(self, mock_jwt_creator, sample_user):
        """Test setting user"""
        builder = TokenBuilder(mock_jwt_creator).for_user(sample_user)

        assert builder._user == sample_user
        assert builder._user.id == 1
        assert builder._user.login == "testuser"

    def test_with_type(self, mock_jwt_creator):
        """Test setting token type"""
        builder = TokenBuilder(mock_jwt_creator).with_type(TokenType.ACCESS)

        assert builder._token_type == TokenType.ACCESS

    def test_with_expire_minutes(self, mock_jwt_creator):
        """Test setting expiration in minutes"""
        builder = TokenBuilder(mock_jwt_creator).with_expire_minutes(30)

        assert builder._expire_minutes == 30

    def test_with_expire_days(self, mock_jwt_creator):
        """Test setting expiration in days"""
        builder = TokenBuilder(mock_jwt_creator).with_expire_days(7)

        assert builder._expire_timedelta == timedelta(days=7)

    def test_method_chaining(self, mock_jwt_creator, sample_user):
        """Test that methods can be chained"""
        builder = (
            TokenBuilder(mock_jwt_creator)
            .for_user(sample_user)
            .with_type(TokenType.ACCESS)
            .with_expire_minutes(30)
        )

        assert builder._user == sample_user
        assert builder._token_type == TokenType.ACCESS
        assert builder._expire_minutes == 30

    def test_build_success(self, mock_jwt_creator, sample_user):
        """Test successful token build"""
        token = (
            TokenBuilder(mock_jwt_creator)
            .for_user(sample_user)
            .with_type(TokenType.ACCESS)
            .build()
        )

        mock_jwt_creator.assert_called_once()
        call_args = mock_jwt_creator.call_args

        assert call_args.kwargs["token_type"] == TokenType.ACCESS
        assert call_args.kwargs["token_data"]["sub"] == sample_user.id
        assert call_args.kwargs["token_data"]["login"] == sample_user.login
        assert call_args.kwargs["token_data"]["username"] == sample_user.name
        assert token == "mock.jwt.token"

    def test_build_missing_token_type(self, mock_jwt_creator, sample_user):
        """Test build fails when token type is missing"""
        builder = TokenBuilder(mock_jwt_creator).for_user(sample_user)

        with pytest.raises(ValueError, match="Token type and user must be set"):
            builder.build()

    def test_build_missing_user(self, mock_jwt_creator):
        """Test build fails when user is missing"""
        builder = TokenBuilder(mock_jwt_creator).with_type(TokenType.ACCESS)

        with pytest.raises(ValueError, match="Token type and user must be set"):
            builder.build()

    def test_create_payload_access_token(self, mock_jwt_creator, sample_user):
        """Test payload creation for access token"""
        builder = (
            TokenBuilder(mock_jwt_creator)
            .for_user(sample_user)
            .with_type(TokenType.ACCESS)
        )

        payload = builder._create_payload()

        expected_payload = {
            "sub": sample_user.id,
            "login": sample_user.login,
            "username": sample_user.name,
        }
        assert payload == expected_payload

    def test_create_payload_refresh_token(self, mock_jwt_creator, sample_user):
        """Test payload creation for refresh token (without username)"""
        builder = (
            TokenBuilder(mock_jwt_creator)
            .for_user(sample_user)
            .with_type(TokenType.REFRESH)
        )

        payload = builder._create_payload()

        expected_payload = {"sub": sample_user.id, "login": sample_user.login}
        assert payload == expected_payload
        assert "username" not in payload

    def test_expiration_parameters_passed_correctly(
        self, mock_jwt_creator, sample_user
    ):
        """Test that expiration parameters are passed to jwt_creator"""
        token = (
            TokenBuilder(mock_jwt_creator)
            .for_user(sample_user)
            .with_type(TokenType.ACCESS)
            .with_expire_minutes(45)
            .build()
        )

        call_args = mock_jwt_creator.call_args
        assert call_args.kwargs["expire_minutes"] == 45
        assert call_args.kwargs["expire_timedelta"] is None

    def test_timedelta_expiration(self, mock_jwt_creator, sample_user):
        """Test that timedelta expiration is passed correctly"""
        token = (
            TokenBuilder(mock_jwt_creator)
            .for_user(sample_user)
            .with_type(TokenType.REFRESH)
            .with_expire_days(30)
            .build()
        )

        call_args = mock_jwt_creator.call_args
        assert call_args.kwargs["expire_timedelta"] == timedelta(days=30)
        assert call_args.kwargs["expire_minutes"] is None
