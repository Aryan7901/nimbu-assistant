
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:nimbu_frontend/utils/commands.dart';

class CommandInput extends StatelessWidget {
  const CommandInput({
    super.key,
    required Color accent,
    required this.cmd,
    required this.commands,
    required this.onChanged

  }) : _accent = accent;

  final Color _accent;
  final Commands cmd;
  final List<Commands> commands;
  final ValueChanged<String> onChanged;

  @override
  Widget build(BuildContext context, ) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.black45,
        borderRadius: const BorderRadius.only(
          bottomLeft: Radius.circular(20),
          bottomRight: Radius.circular(20),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            "COMPUTER COMMAND:",
            style: TextStyle(
              color: _accent,
              fontSize: 10,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.0,
            ),
          ),
          const SizedBox(height: 8),
          TextFormField(
            initialValue: cmd.command,
            style: TextStyle(
              fontFamily: Platform.isIOS ? "Courier" : "monospace",
              color: _accent,
              fontSize: 15,
            ),
            decoration: InputDecoration(
              filled: false,
              hintText: "code .",
              hintStyle: TextStyle(
                color: _accent.withOpacity(0.3),
              ),
              contentPadding: EdgeInsets.zero,
              border: InputBorder.none,
              focusedBorder: InputBorder.none,
            ),
            onChanged:onChanged,
          ),
        ],
      ),
    );
  }
}

