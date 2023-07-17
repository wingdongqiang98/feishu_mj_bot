# coding:utf-8
import logging

LOGGER = logging.getLogger()


CARD_MSG_TEMPLATE = """
{
  "config": {
    "wide_screen_mode": true
  },
  "elements": [
    {
      "tag": "markdown",
      "content": "点击图片下方按钮可进一步处理图片"
    },
    {
      "alt": {
        "content": "",
        "tag": "plain_text"
      },
      "img_key": "${img_key}",
      "tag": "img"
    },
    {
      "tag": "column_set",
      "flex_mode": "none",
      "background_style": "grey",
      "columns": []
    },
    {
      "tag": "div",
      "text": {
        "content": "放大",
        "tag": "plain_text"
      }
    },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "u1"
          },
          "type": "primary",
          "value": {
            "action": "u1",
            "task_id": "${task_id}"
          }
        },
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "u2"
          },
          "type": "primary",
          "value": {
            "action": "u2",
            "task_id": "${task_id}"
          }
        },
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "u3"
          },
          "type": "primary",
          "value": {
            "action": "u3",
            "task_id": "${task_id}"
          }
        },
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "u4"
          },
          "type": "primary",
          "value": {
            "action": "u4",
            "task_id": "${task_id}"
          }
        }
      ]
    },
    {
      "tag": "div",
      "text": {
        "content": "变化",
        "tag": "plain_text"
      }
    },
    {
      "tag": "action",
      "actions": [
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "v1"
          },
          "type": "primary",
          "value": {
            "action": "v1",
            "task_id": "${task_id}"
          }
        },
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "v2"
          },
          "type": "primary",
          "value": {
            "action": "v2",
            "task_id": "${task_id}"
          }
        },
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "v3"
          },
          "type": "primary",
          "value": {
            "action": "v3",
            "task_id": "${task_id}"
          }
        },
        {
          "tag": "button",
          "text": {
            "tag": "plain_text",
            "content": "v4"
          },
          "type": "primary",
          "value": {
            "action": "v4",
            "task_id": "${task_id}"
          }
        }
      ]
    }
  ]
}
"""


def main():
    pass


if __name__ == "__main__":
    main()
