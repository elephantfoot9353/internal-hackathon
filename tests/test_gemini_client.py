import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from ai.gemini_client import GeminiClient


@pytest.fixture
def mock_api_key():
    return "test-api-key-12345"


@pytest.fixture
def gemini_client(mock_api_key):
    with patch("google.generativeai.configure"):
        with patch("google.generativeai.GenerativeModel"):
            client = GeminiClient(mock_api_key)
            return client


class TestGeminiClientInit:
    def test_init_with_api_key(self, mock_api_key):
        with patch("google.generativeai.configure") as mock_configure:
            with patch("google.generativeai.GenerativeModel"):
                client = GeminiClient(mock_api_key)
                mock_configure.assert_called_once_with(api_key=mock_api_key)


class TestGenerateExcuses:
    def test_generate_excuses_success(self, gemini_client):
        mock_response = Mock()
        mock_response.text = json.dumps(
            {
                "excuses": [
                    {
                        "text": "몸이 안 좋아서 못 갈 것 같아",
                        "reaction": "엄마: 또? 증빙 사진 보내줄래?",
                        "grade": "B",
                        "caution": "열은 재지 말고 집에만 있기",
                    },
                    {
                        "text": "급하게 일이 생겼어",
                        "reaction": "친구: 뭔데?",
                        "grade": "C",
                        "caution": "구체적 내용 물어볼 때 대답 준비하기",
                    },
                    {
                        "text": "교통사고가 나 근처 있어",
                        "reaction": "상사: 확인해봐야겠는데?",
                        "grade": "D",
                        "caution": "인스타는 절대 금지",
                    },
                    {
                        "text": "혼자가 아니라 누군가가 나를 잡아둬",
                        "reaction": "모두: ???",
                        "grade": "F",
                        "caution": "이 변명은 사용하지 마세요",
                    },
                ]
            }
        )

        gemini_client.model.generate_content = Mock(return_value=mock_response)

        result = gemini_client.generate_excuses("약속", 7, 5)

        assert "excuses" in result
        assert len(result["excuses"]) == 4
        assert result["excuses"][0]["text"] == "몸이 안 좋아서 못 갈 것 같아"
        assert result["excuses"][0]["grade"] == "B"

    def test_generate_excuses_with_markdown_json(self, gemini_client):
        mock_response = Mock()
        mock_response.text = """```json
{
    "excuses": [
        {
            "text": "변명",
            "reaction": "반응",
            "grade": "A",
            "caution": "주의사항"
        }
    ]
}
```"""

        gemini_client.model.generate_content = Mock(return_value=mock_response)

        result = gemini_client.generate_excuses("과제", 5, 3)

        assert "excuses" in result
        assert len(result["excuses"]) == 1
        assert result["excuses"][0]["grade"] == "A"

    def test_generate_excuses_invalid_json(self, gemini_client):
        mock_response = Mock()
        mock_response.text = "This is not JSON"

        gemini_client.model.generate_content = Mock(return_value=mock_response)

        with pytest.raises(ValueError, match="AI 응답을 JSON으로 파싱할 수 없습니다"):
            gemini_client.generate_excuses("약속", 5, 5)

    def test_generate_excuses_politeness_levels(self, gemini_client):
        mock_response = Mock()
        mock_response.text = json.dumps({"excuses": []})

        gemini_client.model.generate_content = Mock(return_value=mock_response)
        gemini_client.model.generate_content.reset_mock()

        # 낮은 정중함
        gemini_client.generate_excuses("약속", 2, 5)
        call_args = gemini_client.model.generate_content.call_args[0][0]
        assert "반말로 편하게" in call_args

        gemini_client.model.generate_content.reset_mock()

        # 높은 정중함
        gemini_client.generate_excuses("약속", 9, 5)
        call_args = gemini_client.model.generate_content.call_args[0][0]
        assert "존댓말로 매우 정중하게" in call_args

    def test_generate_excuses_credibility_levels(self, gemini_client):
        mock_response = Mock()
        mock_response.text = json.dumps({"excuses": []})

        gemini_client.model.generate_content = Mock(return_value=mock_response)
        gemini_client.model.generate_content.reset_mock()

        # 낮은 신뢰도
        gemini_client.generate_excuses("약속", 5, 2)
        call_args = gemini_client.model.generate_content.call_args[0][0]
        assert "명백히 거짓 같지만 유머러스하게" in call_args

        gemini_client.model.generate_content.reset_mock()

        # 높은 신뢰도
        gemini_client.generate_excuses("약속", 5, 9)
        call_args = gemini_client.model.generate_content.call_args[0][0]
        assert "그럴듯하고 믿음직스럽게" in call_args


class TestGenerateDefenseResponse:
    def test_generate_defense_response_success(self, gemini_client):
        mock_response = Mock()
        mock_response.text = json.dumps({"defense": "증명할 수 있는 뭔가를 준비했어"})

        gemini_client.model.generate_content = Mock(return_value=mock_response)

        result = gemini_client.generate_defense_response(
            original_excuse="몸이 안 좋아",
            opponent_reaction="그럼 병원가서 증명서 가져와",
            attempt_count=1,
        )

        assert result == "증명할 수 있는 뭔가를 준비했어"

    def test_generate_defense_response_with_markdown(self, gemini_client):
        mock_response = Mock()
        mock_response.text = """```json
{"defense": "상황 설명"}
```"""

        gemini_client.model.generate_content = Mock(return_value=mock_response)

        result = gemini_client.generate_defense_response(
            original_excuse="일이 있었어",
            opponent_reaction="거짓말이지?",
            attempt_count=2,
        )

        assert result == "상황 설명"

    def test_generate_defense_response_invalid_json_fallback(self, gemini_client):
        mock_response = Mock()
        mock_response.text = "Just a plain text response"

        gemini_client.model.generate_content = Mock(return_value=mock_response)

        result = gemini_client.generate_defense_response(
            original_excuse="변명",
            opponent_reaction="의심스러워",
            attempt_count=1,
        )

        assert result == "Just a plain text response"

    def test_generate_defense_response_missing_defense_key(self, gemini_client):
        mock_response = Mock()
        mock_response.text = json.dumps({"other_key": "value"})

        gemini_client.model.generate_content = Mock(return_value=mock_response)

        result = gemini_client.generate_defense_response(
            original_excuse="변명", opponent_reaction="의심", attempt_count=1
        )

        assert result == ""
