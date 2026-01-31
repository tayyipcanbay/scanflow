---
description: Scaffold a new Feature Module following the project architecture
---

To use this workflow, you need to provide a MODULE_NAME.

1. Create Module Directory
```bash
mkdir -p lib/modules/${MODULE_NAME}
```

2. Create Module Manifest (manifest.json)
```bash
echo '{
  "id": "${MODULE_NAME}",
  "name": "${MODULE_NAME}",
  "type": "INTERNAL_CORE",
  "enabled": true
}' > lib/modules/${MODULE_NAME}/manifest.json
```

3. Create Module Widget File
```bash
echo "import 'package:flutter/material.dart';

class ${MODULE_NAME}Widget extends StatelessWidget {
  const ${MODULE_NAME}Widget({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(child: Text('${MODULE_NAME} Module'));
  }
}" > lib/modules/${MODULE_NAME}/${MODULE_NAME}_widget.dart
```

4. Create Module Logic File (Service/Controller)
```bash
echo "class ${MODULE_NAME}Service {
  // Business logic for ${MODULE_NAME}
}" > lib/modules/${MODULE_NAME}/${MODULE_NAME}_service.dart
```
