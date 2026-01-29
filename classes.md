# Agent365 Python Classes Documentation

This document provides an overview of all classes in the Agent365 Python codebase, organized by library.

> **Note:** Class names are documented exactly as they appear in the source code. Some naming inconsistencies (e.g., `Mcp` vs `MCP`) reflect the actual implementation.

## Tooling Library

### McpToolServerConfigurationService
Service for discovering and configuring MCP (Model Context Protocol) tool servers from local manifests or remote gateway endpoints in both dev and production scenarios.

### MCPServerConfig
Dataclass representing MCP server configuration with name and unique endpoint.

### ToolOptions
Configuration options dataclass for tooling operations including orchestrator name.

### Constants
Constant values for HTTP headers and authentication used throughout tooling components.

## Observability Core Library

### TelemetryManager
Thread-safe singleton managing OpenTelemetry configuration, tracing, and span processors for telemetry operations.

### OpenTelemetryScope
Base class for OpenTelemetry tracing scopes with span creation, attribute setting, and error recording.

### InferenceScope
Extends OpenTelemetryScope for tracing generative AI inference operations with request/response tracking.

### InvokeAgentScope
Extends OpenTelemetryScope for tracing agent invocation operations.

### ExecuteToolScope
Extends OpenTelemetryScope for tracing tool execution operations.

### AgentDetails
Dataclass containing agent metadata including ID, name, type, tenant, and blueprint information.

### TenantDetails
Dataclass representing tenant information for telemetry tracking.

### Request
Dataclass for agent execution request details including content, execution type, and source metadata.

### InferenceCallDetails
Dataclass containing inference operation details for telemetry.

### ToolCallDetails
Dataclass for tool call execution details and metrics.

### SourceMetadata
Dataclass for source-specific metadata in operations.

### InvokeAgentDetails
Dataclass with agent invocation details.

### SpanProcessor
Custom OpenTelemetry BaseSpanProcessor for processing SDK-specific spans.

### _Agent365Exporter
Internal SpanExporter implementation for exporting telemetry to Agent365 infrastructure.

### Agent365ExporterOptions
Dataclass for Agent365 exporter configuration options.

### DictWithLock
Thread-safe dictionary wrapper using locks for concurrent access.

### BaggageBuilder
Builder class for constructing OpenTelemetry baggage context.

### BaggageScope
Context manager for baggage scope management.

### ExecutionType
Enum defining execution operation types.

### ToolType
Enum for tool types in the system.

### InferenceOperationType
Enum for inference operation types.

### AgentType
Enum representing different agent types.

### OperationSource
Enum for operation source types.

### CallerDetails
Dataclass for caller information in telemetry.

## Notifications Library

### AgentNotification
Provides decorated routing for agent notifications across different channels (Email, Word, Excel, PowerPoint) and lifecycle events.

### AgentNotificationActivity
Dataclass representing an agent notification activity.

### AgentSubChannel
Enum for notification subchannels (Email, Word, Excel, PowerPoint, etc.).

### AgentLifecycleEvent
Enum for agent lifecycle events (UserCreated, UserDeleted, UserWorkloadOnboardingUpdated).

### NotificationTypes
Enum for notification type classifications.

### EmailReference
Entity dataclass for email message references.

### EmailResponse
Entity dataclass for email response data.

### WpxComment
Entity dataclass for comment metadata from Office applications.

## Runtime Library

### PowerPlatformApiDiscovery
Discovery helper for Power Platform API endpoints based on cluster category and tenant identification.

### Utility
Utility class for runtime operations.

## Observability Hosting Library

### AgenticTokenStruct
Dataclass containing token generation components (authorization and turn context).

### AgenticTokenCache
Thread-safe cache for observability tokens keyed by (agentId, tenantId) with lazy token exchange.

## Observability Extension Libraries

### SemanticKernel Extensions

#### SemanticKernelInstrumentor
OpenTelemetry instrumentor for SemanticKernel framework tracing integration.

#### SemanticKernelSpanProcessor
Custom span processor for SemanticKernel tracing operations.

### OpenAI Extensions

#### OpenAIAgentsTraceInstrumentor
Instrumentor for OpenAI agents framework telemetry integration.

#### OpenAIAgentsTraceProcessor
Span processor for OpenAI agents tracing operations.

#### MCPServerInfo
Configuration information for MCP servers in OpenAI context.

### AgentFramework Extensions

#### AgentFrameworkInstrumentor
Instrumentor for AgentFramework telemetry integration.

#### AgentFrameworkSpanProcessor
Span processor for AgentFramework tracing operations.

### LangChain Extensions

#### CustomLangChainInstrumentor
Instrumentor for LangChain framework telemetry integration.

#### CustomLangChainTracer
Custom tracer for LangChain operations and callbacks.

#### _BaseCallbackManagerInit
Internal helper for LangChain callback manager initialization.

## Tooling Extension Libraries

### McpToolRegistrationService
Service for registering MCP tools with various AI frameworks including AgentFramework, SemanticKernel, OpenAI, and AzureAIFoundry.

---

*This documentation was generated to provide a high-level overview of the class structure in the Agent365 Python codebase.*
