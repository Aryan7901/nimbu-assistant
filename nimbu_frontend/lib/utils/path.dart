import 'dart:io';

import 'package:path/path.dart' as p;

String getNimbuPath() {
  String home = Platform.isWindows 
      ? Platform.environment['USERPROFILE']! 
      : Platform.environment['HOME']!;

  // This function detects the OS and picks the right slash!
  return p.join(home, ".nimbu", "commands.json");
}