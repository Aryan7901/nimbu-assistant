
import 'package:flutter/material.dart';
import 'package:nimbu_frontend/components/ActionNameInput.dart';
import 'package:nimbu_frontend/components/CommandInput.dart';
import 'package:nimbu_frontend/utils/commands.dart';

class CommandsList extends StatelessWidget {
  const CommandsList({
    super.key,
    required this.commands,
    required Color cardColor,
    required Color accentYellow,
    required Color accentGreen,
    required this.onPressed,
  }) : _cardColor = cardColor,
       _accentYellow = accentYellow,
       _accentGreen = accentGreen;

  final List<Commands> commands;
  final Color _cardColor;
  final Color _accentYellow;
  final Color _accentGreen;
  final ValueChanged<int> onPressed;

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      padding: const EdgeInsets.fromLTRB(16, 10, 16, 100),
      itemCount: commands.length,
      itemBuilder: (context, index) {
        final cmd = commands[index];
        return Container(
          margin: const EdgeInsets.only(bottom: 20),
          decoration: BoxDecoration(
            color: _cardColor,
            borderRadius: BorderRadius.circular(20),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.3),
                blurRadius: 10,
                offset: const Offset(0, 5),
              ),
            ],
            border: Border.all(color: Colors.grey[800]!),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Align(
                alignment: Alignment.topRight,
                child: IconButton(
                  icon: const Icon(Icons.close, color: Colors.redAccent),
                  onPressed: () => onPressed(index),
                ),
              ),

              ActionNameInput(
                accentYellow: _accentYellow,
                cmd: cmd,
                commands: commands,
                onChanged: (v) => commands[index].name = v,
              ),

              const SizedBox(height: 20),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: TextFormField(
                  initialValue: cmd.description,
                  style: const TextStyle(fontSize: 16),
                  decoration: const InputDecoration(
                    prefixIcon: Icon(Icons.mic, color: Colors.grey),
                    labelText: "What does this do?",
                    hintText: "e.g. 'Opens Visual Studio Code'",
                    filled: true,
                    fillColor: Colors.black12,
                  ),
                  onChanged: (v) => commands[index].description = v,
                ),
              ),

              const SizedBox(height: 16),
              CommandInput(
                accent: _accentGreen,
                cmd: cmd,
                commands: commands,
                onChanged: (v) => commands[index].command = v,
              ),
            ],
          ),
        );
      },
    );
  }
}
