class Commands {
  String description;
  String command;
  String name;
  Commands({
    required this.name,
    required this.description,
    required this.command,
  });

  factory Commands.fromJson(Map<String, dynamic> json) {
    return Commands(
      name: json['name'] as String,
      description: json['description'] as String,
      command: json['command'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {'name': name, 'description': description, 'command': command};
  }
}
