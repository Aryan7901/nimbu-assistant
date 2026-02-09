import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:nimbu_frontend/components/CommandsList.dart';
import 'package:nimbu_frontend/components/EmptyState.dart';
import 'package:nimbu_frontend/constants/colors.dart';
import 'package:nimbu_frontend/utils/commands.dart';
import 'package:nimbu_frontend/utils/path.dart';

void main() => runApp(const MaterialApp(home: NimbuConfigEditor()));

class NimbuConfigEditor extends StatefulWidget {
  const NimbuConfigEditor({super.key});

  @override
  State<NimbuConfigEditor> createState() => _NimbuConfigEditorState();
}

class _NimbuConfigEditorState extends State<NimbuConfigEditor> {
  List<Commands> commands = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadConfig();
  }

  Future<File> _getConfigFile() async {
    final path = await getNimbuPath();
    return File(path);
  }

  Future<void> _loadConfig() async {
    final file = await _getConfigFile();
    if (await file.exists()) {
      try {
        final content = await file.readAsString();
        Map<String, dynamic> jsonMap = jsonDecode(content);
        List<dynamic> commandsJson = jsonMap['custom_commands'] ?? [];

        setState(() {
          commands = List<Commands>.from(
            commandsJson.map((item) => Commands.fromJson(item)),
          );
          isLoading = false;
        });
      } catch (e) {
        // If JSON is broken, start fresh but don't crash
        setState(() {
          commands = [];
          isLoading = false;
        });
        debugPrint("Error loading config: $e");
      }
    } else {
      setState(() {
        commands = [];
        isLoading = false;
      });
    }
  }

  Future<void> _saveConfig() async {
    // Basic validation: Don't save if names are empty
    if (commands.any((c) => c.name.trim().isEmpty)) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          backgroundColor: Colors.redAccent,
          content: Text("Error: All commands must have a Nickname (ID)."),
        ),
      );
      return;
    }

    final file = await _getConfigFile();
    final data = {"custom_commands": commands};

    await file.writeAsString(const JsonEncoder.withIndent('  ').convert(data));

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          backgroundColor: Colors.limeAccent[400],
          content: const Text(
            "Nimbu updated! Daemon will reload.",
            style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold),
          ),
          behavior: SnackBarBehavior.floating,
        ),
      );
    }
  }



  @override
  Widget build(BuildContext context) {
    return Theme(
      data: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: bgColor,
        primaryColor: accentYellow,
        colorScheme: ColorScheme.dark(
          primary: accentYellow,
          secondary: accentGreen,
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: bgColor,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide.none,
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: BorderSide(color: accentYellow, width: 2),
          ),
          contentPadding: const EdgeInsets.symmetric(
            horizontal: 20,
            vertical: 16,
          ),
        ),
      ),
      child: Scaffold(
        appBar: AppBar(
          backgroundColor: Colors.transparent,
          elevation: 0,
          centerTitle: true,
          title: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              const SizedBox(width: 8),
              Text(
                "NIMBU EDITOR",
                style: TextStyle(
                  color: accentYellow,
                  fontWeight: FontWeight.w900,
                  letterSpacing: 2.0,
                  fontSize: 18,
                ),
              ),
            ],
          ),
          actions: [
            Container(
              margin: const EdgeInsets.only(right: 16),
              decoration: BoxDecoration(
                color: accentGreen.withOpacity(0.2),
                shape: BoxShape.circle,
              ),
              child: IconButton(
                icon: Icon(Icons.save_rounded, color: accentGreen),
                tooltip: "Save Config",
                onPressed: _saveConfig,
              ),
            ),
          ],
        ),
        body: isLoading
            ? Center(child: CircularProgressIndicator(color: accentYellow))
            : commands.isEmpty
            ? EmptyState()
            : CommandsList(
                commands: commands,
                cardColor: cardColor,
                accentYellow: accentYellow,
                accentGreen: accentGreen,
                onPressed: (index) => setState(() => commands.removeAt(index)),
              ),
        floatingActionButton: FloatingActionButton.extended(
          backgroundColor: accentYellow,
          elevation: 10,
          onPressed: () => setState(
            () => commands.add(
              Commands(name: "", description: "", command: ""),
            ),
          ),
          label: const Text(
            "NEW COMMAND",
            style: TextStyle(
              color: Colors.black,
              fontWeight: FontWeight.bold,
              letterSpacing: 1.0,
            ),
          ),
          icon: const Icon(Icons.add_circle_outline, color: Colors.black),
        ),
      ),
    );
  }
}
