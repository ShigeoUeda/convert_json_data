import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

def parse_coordinates(coord_str: str) -> Tuple[float, float]:
    """
    座標文字列をx,y座標に分解

    Args:
        coord_str (str): "x,y"形式の座標文字列

    Returns:
        Tuple[float, float]: (x座標, y座標)のタプル

    Raises:
        ValueError: 座標文字列のフォーマットが不正な場合
    """
    try:
        x, y = map(float, coord_str.split(','))
        return x, y
    except ValueError as e:
        raise ValueError(f"Invalid coordinate format: {coord_str}") from e

def convert_node(node: Dict) -> Dict:
    """
    ノードデータを新しいフォーマットに変換

    Args:
        node (Dict): 変換前のノードデータ

    Returns:
        Dict: 変換後のノードデータ

    Raises:
        KeyError: 必要なキーが存在しない場合
        ValueError: 座標解析に失敗した場合
    """
    x, y = parse_coordinates(node['coord'])
    
    return {
        'id': node['nodeId'].replace('#', ''),
        'width': int(node['width']),
        'height': int(node['height']),
        'position_x': x,
        'position_y': y,
        'label': node['content'],
        'nodeType': node['type']
    }

def convert_link(link: Dict) -> Dict:
    """
    リンクデータを新しいフォーマットに変換

    Args:
        link (Dict): 変換前のリンクデータ

    Returns:
        Dict: 変換後のリンクデータ
    """
    return {
        'id': link['linkId'].replace('#', ''),
        'source': link['sourceNodeId'].replace('#', ''),
        'target': link['targetNodeId'].replace('#', ''),
        'linkType': link['propertyName'] if link['propertyName'] else ""
    }

def convert_json_format(input_file: Path, output_file: Path) -> None:
    """
    JSONファイルを変換して新しいフォーマットで保存

    Args:
        input_file (Path): 入力JSONファイルのパス
        output_file (Path): 出力JSONファイルのパス

    Raises:
        FileNotFoundError: 入力ファイルが存在しない場合
        json.JSONDecodeError: JSONの解析に失敗した場合
        IOError: ファイルの読み書きに失敗した場合
    """
    # 入力ファイルを読み込み
    with input_file.open('r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 新しいフォーマットのデータを作成
    converted_data = {
        'nodes': [convert_node(node) for node in data['nodeList']],
        'links': [convert_link(link) for link in data['linkList']]
    }
    
    # 結果を出力ファイルに保存
    with output_file.open('w', encoding='utf-8') as f:
        json.dump(converted_data, f, ensure_ascii=False, indent=4)

def main() -> None:
    """
    メイン処理を実行

    コマンドライン引数を解析し、JSONファイルの変換を実行します。
    """
    parser = argparse.ArgumentParser(
        description='Convert JSON format from summary.json format to result.json format'
    )
    parser.add_argument(
        'input_file',
        type=Path,
        help='Input JSON file path in summary.json format'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('analysis_result_0001.json'),
        help='Output JSON file path (default: analysis_result_0001.json)'
    )

    args = parser.parse_args()

    try:
        convert_json_format(args.input_file, args.output)
        print(f"Conversion completed. Output saved to {args.output}")
    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON from '{args.input_file}'")
        exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
