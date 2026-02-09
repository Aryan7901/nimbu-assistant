
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:nimbu_frontend/utils/commands.dart';


class LowerCaseTextFormatter extends TextInputFormatter {
  @override
  TextEditingValue formatEditUpdate(
    TextEditingValue oldValue,
    TextEditingValue newValue,
  ) {
    // 1. Force lowercase
    // 2. Replace spaces with underscores
    String newString = newValue.text.toLowerCase().replaceAll(' ', '_');

    // 3. Prevent double underscores (optional, but cleaner)
    newString = newString.replaceAll('__', '_');

    return TextEditingValue(
      text: newString,
      selection: TextSelection.collapsed(offset: newString.length),
    );
  }
}

class ActionNameInput extends StatelessWidget {
  const ActionNameInput({
    super.key,
    required Color accentYellow,
    required this.cmd,
    required this.commands,
    required this.onChanged
  }) : _accentYellow = accentYellow;

  final Color _accentYellow;
  final Commands cmd;
  final List<Commands> commands;
  final ValueChanged<String> onChanged;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: Row(
        children: [
          Icon(Icons.tag, color: _accentYellow, size: 24),
          const SizedBox(width: 12),
          Expanded(
            child: TextFormField(
              initialValue: cmd.name,
              inputFormatters: [
                FilteringTextInputFormatter.allow(
                  RegExp("[a-zA-Z0-9_]"),
                ),
                LowerCaseTextFormatter(),
              ],
              style: TextStyle(
                color: _accentYellow,
                fontWeight: FontWeight.bold,
                fontSize: 18,
              ),
              decoration: InputDecoration(
                labelText: "Action Nickname (ID)",
                labelStyle: TextStyle(color: Colors.grey[400]),
                hintText: "e.g. open_code_editor",
                helperText: "Short name. Should convey purpose. No spaces allowed.",
                helperStyle: TextStyle(color: Colors.grey[600]),
                border: InputBorder.none,
                enabledBorder: UnderlineInputBorder(
                  borderSide: BorderSide(color: Colors.grey[700]!),
                ),
                focusedBorder: UnderlineInputBorder(
                  borderSide: BorderSide(color: _accentYellow),
                ),
                filled: false,
                contentPadding: const EdgeInsets.symmetric(
                  vertical: 8,
                ),
              ),
              onChanged: onChanged,
            ),
          ),
        ],
      ),
    );
  }
}
