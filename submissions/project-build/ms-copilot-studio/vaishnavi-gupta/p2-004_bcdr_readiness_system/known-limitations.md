# Known Limitations

- The solution depends on the availability of Microsoft Copilot Studio services and configured connectors.
- Technical recommendations rely on the Microsoft Learn MCP Server. If the MCP service is unavailable, technical validation may be limited.
- The system assesses only applications and data available in the configured Excel workbook.
- Assessment quality depends on the accuracy and completeness of the provided business and technical information.
- The File Modified Trigger executes only when changes are detected in the monitored folder.
- The solution does not perform live infrastructure discovery or direct Azure environment validation.
- Report generation and email notifications require properly configured Microsoft Word and Outlook connections.
- The current implementation is designed for the project scope and may require additional customization for enterprise-scale deployments.