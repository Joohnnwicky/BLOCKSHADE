"""Flask Blueprint routes for TRON analysis tools"""

from flask import Blueprint, jsonify, request, Response
from .suspicious_analyzer import analyze_address_web, is_valid_tron_address
from modules.core.exporter import export_json, export_csv

tron_bp = Blueprint('tron', __name__, url_prefix='/tron')

@tron_bp.route('/api/analyze', methods=['POST'])
def analyze():
    """API endpoint for TRON address suspicious feature analysis.

    Request JSON body: {"address": "TRON_ADDRESS"}
    Response JSON: {
        "success": bool,
        "address": str,
        "basic_info": dict,
        "alerts": {"red": [], "yellow": [], "green": [], "score": int}
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': '请提供JSON数据'}), 400

    address = data.get('address', '')
    if not address:
        return jsonify({'success': False, 'error': '请提供TRON地址'}), 400

    result = analyze_address_web(address)

    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

@tron_bp.route('/api/sample')
def get_sample():
    """Return sample TRON address for user input format demonstration.

    Response JSON: {"address": str, "description": str}
    """
    return jsonify({
        'address': 'TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw',
        'description': '示例TRON地址，点击"加载样本"按钮填充'
    })

@tron_bp.route('/api/export/json', methods=['POST'])
def export_json_endpoint():
    """Export analysis result as JSON file download.

    Request JSON body: {"result": analysis_result_dict}
    Response: JSON file download with Content-Disposition header
    """
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供分析结果数据'}), 400

    result = data['result']
    address = result.get('address', 'unknown')

    json_content = export_json(result)

    from modules.core.exporter import get_export_filename
    filename = get_export_filename(address, 'json')

    response = Response(
        json_content,
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response

@tron_bp.route('/api/export/csv', methods=['POST'])
def export_csv_endpoint():
    """Export analysis alerts as CSV file download.

    Request JSON body: {"result": analysis_result_dict}
    Response: CSV file download with Content-Disposition header
    """
    data = request.get_json()
    if not data or 'result' not in data:
        return jsonify({'error': '请提供分析结果数据'}), 400

    result = data['result']
    address = result.get('address', 'unknown')

    csv_content = export_csv(result)

    from modules.core.exporter import get_export_filename
    filename = get_export_filename(address, 'csv')

    response = Response(
        csv_content,
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
    return response