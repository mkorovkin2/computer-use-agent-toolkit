# Computer Use Agent Toolkit - Examples

This directory contains examples demonstrating the Computer Use Agent SDK in both Python and TypeScript.

## 📁 Structure

- **`python/`** - Python examples
- **`typescript/`** - TypeScript examples

## 🚀 Quick Start

### Python

```bash
# Install the package
cd python
pip install -e .

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run an example
cd ../examples/python
python 01_simple_click.py
```

### TypeScript

```bash
# Install dependencies
cd typescript
npm install
npm run build

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run an example
cd ../examples/typescript
npx ts-node 01_simple_click.ts
```

## 📚 Examples

### Basic Examples

1. **Simple Click** - Click on a screen element
2. **Form Filler** - Fill out forms with multiple fields
3. **Browser Navigator** - Navigate websites and extract information

### Advanced Examples

4. **Custom Tools** - Register custom tools for database queries, APIs, etc.
5. **Workflow Hooks** - Add logging, metrics, and conditional logic
6. **Multi-System Integration** - Combine UI interaction with backend systems
7. **Human-in-the-Loop** - Add approval gates for sensitive operations
8. **Data Extraction** - Extract data from applications and save to files
9. **Cross-Application** - Work across multiple applications
10. **Error Recovery** - Implement retry logic and error handling

## 🎯 Learning Path

**Beginner:**
1. Start with `01_simple_click` to understand basic agent usage
2. Try `02_form_filler` to see multi-step interactions
3. Explore `03_browser_navigator` for more complex tasks

**Intermediate:**
4. Learn `04_custom_tools` to extend agent capabilities
5. Study `05_workflow_hooks` for logging and metrics
6. Review `06_multi_system_integration` for real-world patterns

**Advanced:**
7. Implement `07_human_in_the_loop` for production safety
8. Build on `08_data_extraction` for automation workflows
9. Explore `09_cross_application` for complex scenarios
10. Master `10_error_recovery` for robust agents

## 💡 Tips

- **Always start in dry-run mode** when testing new workflows
- **Use hooks** for debugging and understanding agent behavior
- **Set max_iterations** appropriately to prevent runaway agents
- **Test on non-critical data** first
- **Add logging** to track agent decisions

## 📖 Documentation

For detailed API documentation, see the [main README](../README.md).

## 🛡️ Safety

All examples include safety features:
- Rate limiting between actions
- Optional confirmation modes
- Error handling
- Restricted action regions (where applicable)

## 🤝 Contributing

Have a great example? Submit a PR! Make sure to:
- Include clear comments
- Add error handling
- Follow the existing structure
- Test on multiple platforms if possible

