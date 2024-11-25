import json
from datetime import datetime, timezone
import uuid

def generate_edge_data(id, label, source, target, editor_name, creator_editor_id_suffix=None):
    # 現在のUTC時刻を取得し、指定された形式に変換
    current_time = datetime.now(timezone.utc)
    utc_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    local_time = current_time.astimezone().strftime("%Y/%m/%d %H:%M:%S")

    # ユニークなIDを生成（タイムスタンプ + ランダムな文字列）
    # edge_id = f"#{current_time.strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:4]}"

    # creatorとeditorの共通IDを設定
    creator_editor_id_suffix = creator_editor_id_suffix or uuid.uuid4().hex[:10]
    creator_editor_id = f"graphCollab:{creator_editor_id_suffix}"

    # 新しいエッジデータを生成
    edge_data = {
        "type": "graphEdge",
        "markerEnd": {
            "width": 20.0,
            "height": 20.0,
            "type": "arrowclosed"
        },
        "label": label,
        "target": target,
        "id": id,
        "sourceHandle": None,
        "source": source,
        "targetHandle": None,
        "data": {
            "creator": creator_editor_id,
            "lastModified": utc_time,
            "editor": creator_editor_id,
            "creatorName": editor_name,
            "begin": local_time,
            "editorName": editor_name
        }
    }

    return edge_data

# 使用例
if __name__ == "__main__":
    # 新しいエッジデータを生成
    new_edge = generate_edge_data(
        id="edge1",
        label="背景",
        source="#20240919021731_LPQc",
        target="#20240919021734_JCeI",
        editor_name="268",
        creator_editor_id_suffix="ynlbxzlpBN"
    )

    # 生成されたエッジデータを表示
    print(json.dumps(new_edge, indent=2, ensure_ascii=False))

    # 生成されたデータからidを取り出す
    edge_id = new_edge["id"]
    print(f"\n生成されたエッジID: {edge_id}")