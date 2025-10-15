# ROMILLM Communication Protocols

## 📡 Component Communication Architecture

The ROMILLM system implements multiple communication patterns optimized for different interaction types within the cognitive pipeline. Communication protocols are designed around the core architectural principles of performance, reliability, and observability.

---

## 🎯 Communication Pattern Matrix

| **Pattern** | **Use Case** | **Components** | **Performance** | **Reliability** |
|-------------|--------------|----------------|-----------------|-----------------|
| **Observer** | System monitoring | PerformanceMonitor ↔ All | High | Eventual |
| **Strategy** | Search flexibility | SearchContext → Strategies | High | Synchronous |
| **Factory** | Component creation | Factory → Components | High | Synchronous |
| **Mediator** | Pipeline coordination | PipelineManager ↔ Stages | Medium | Synchronous |
| **Command** | Processing workflow | QueryProcessor → Commands | Medium | Synchronous |
| **Publisher-Subscriber** | Event distribution | EventBus → Subscribers | Medium | Asynchronous |

---

## 📊 Observer Pattern Implementation (Performance Monitoring)

### ProcessMetricsSubject Interface

```cpp
class ProcessMetricsSubject {
public:
    virtual ~ProcessMetricsSubject() = default;

    // Observer Management
    void attach(std::shared_ptr<PerformanceObserver> observer);
    void detach(std::shared_ptr<PerformanceObserver> observer);
    void notifyAll(const MetricsSnapshot& metrics) const;

    // Subject State
    MetricsSnapshot getCurrentMetrics() const;
    void setMetricsChanged(bool changed = true);

protected:
    // Template Method Pattern for specialized notifications
    virtual void prepareMetricsNotification(MetricsSnapshot& metrics) = 0;
    virtual bool shouldNotify() const { return metrics_changed_; }

private:
    std::vector<std::weak_ptr<PerformanceObserver>> observers_;
    bool metrics_changed_ = false;
    mutable std::mutex observers_mutex_;
};
```

### PerformanceObserver Implementation

```cpp
class PerformanceObserver : public std::enable_shared_from_this<PerformanceObserver> {
public:
    virtual ~PerformanceObserver() = default;

    // Core Observer Interface
    virtual void onMetricsUpdate(const MetricsSnapshot& metrics) = 0;
    virtual void onError(const ComponentError& error) = 0;
    virtual void onConfigChange(const ConfigurationChange& change) = 0;

    // Observer Metadata
    virtual ObserverPriority getPriority() const { return ObserverPriority::NORMAL; }
    virtual std::string getObserverName() const = 0;

protected:
    // Safe update pattern preventing stack overflow
    void updateSafely(const std::function<void()>& update_func) {
        try {
            update_func();
        } catch (const std::exception& e) {
            logError("Observer update failed", e.what());
        }
    }

    // Helper method for descendant observers
    void logError(const std::string& context, const std::string& error) const;
};
```

### Concrete Performance Monitor Implementation

```cpp
class PerformanceMonitor : public ProcessMetricsSubject {
public:
    // Singleton pattern for system-wide monitoring
    static PerformanceMonitor& getInstance();

    // PerformanceObserver interface override
    void onMetricsUpdate(const MetricsSnapshot& metrics) override;
    void onError(const ComponentError& error) override;
    void onConfigChange(const ConfigurationChange& change) override;

    // Specialized monitoring methods
    void recordQueryPerformance(const QueryId& id,
                               std::chrono::milliseconds duration,
                               QueryIntent intent);

    void recordMemoryUsage(const std::string& component_name,
                          size_t bytes_used,
                          MemoryType type);

    void recordSearchPerformance(const SearchStrategy& strategy,
                               size_t results_count,
                               std::chrono::milliseconds duration);

private:
    // Specialized preparation for performance metrics
    void prepareMetricsNotification(MetricsSnapshot& metrics) override;

    // Performance data storage
    std::unordered_map<QueryId, QueryPerformanceData> query_performance_;
    std::unordered_map<std::string, ComponentMemoryData> component_memory_;
    std::unordered_map<SearchStrategy, SearchPerformanceData> search_performance_;

    // Thread-safe data structures
    mutable std::shared_mutex data_mutex_;
};
```

---

## 🎨 Strategy Pattern Implementation (Search Strategies)

### ISearchStrategy Abstract Interface

```cpp
class ISearchStrategy {
public:
    virtual ~ISearchStrategy() = default;

    // Core Strategy Contract
    virtual SearchResult search(const StructuredQuery& query) = 0;
    virtual SearchType getStrategyType() const noexcept = 0;
    virtual double estimateCost(const StructuredQuery& query) const = 0;
    virtual bool initialize(const SearchConfiguration& config) = 0;

    // Performance & Monitoring
    virtual SearchMetrics getMetrics() const = 0;
    virtual void resetMetrics() = 0;
    virtual bool isHealthy() const noexcept = 0;

    // Resource Management
    virtual size_t getMemoryUsage() const = 0;
    virtual void optimizeResources() = 0;

protected:
    // Template method for common search workflow
    SearchResult executeSearchWithMetrics(const StructuredQuery& query) {
        auto start_time = std::chrono::high_resolution_clock::now();
        SearchResult result = performSearch(query);
        auto end_time = std::chrono::high_resolution_clock::now();

        updateMetrics(result, std::chrono::duration_cast<std::chrono::milliseconds>(
                                                                end_time - start_time));
        return result;
    }

    // Strategy-specific implementation
    virtual SearchResult performSearch(const StructuredQuery& query) = 0;
    virtual void updateMetrics(const SearchResult& result,
                              std::chrono::milliseconds duration) = 0;
};
```

### Vector Search Strategy Implementation

```cpp
class VectorSearchStrategy : public ISearchStrategy {
public:
    VectorSearchStrategy(std::shared_ptr<FAISSIndex> index,
                        std::shared_ptr<EmbeddingGenerator> embedder);

    // ISearchStrategy implementation
    SearchResult search(const StructuredQuery& query) override;
    SearchType getStrategyType() const noexcept override { return SearchType::VECTOR; }
    double estimateCost(const StructuredQuery& query) const override;
    bool initialize(const SearchConfiguration& config) override;

    SearchMetrics getMetrics() const override { return metrics_; }
    void resetMetrics() override;
    bool isHealthy() const noexcept override;
    size_t getMemoryUsage() const override;
    void optimizeResources() override;

private:
    // Vector search specific methods
    SearchResult performSearch(const StructuredQuery& query) override;
    void updateMetrics(const SearchResult& result,
                      std::chrono::milliseconds duration) override;

    std::vector<float> generateEmbedding(const std::string& text) const;
    std::vector<faiss::idx_t> findSimilarVectors(
        const std::vector<float>& query_embedding, int k) const;

    // Vector-specific optimizations
    void optimizeIndexIfNecessary();
    void updateIndexStatistics(const SearchResult& result);

    // Member variables
    std::shared_ptr<FAISSIndex> faiss_index_;
    std::shared_ptr<EmbeddingGenerator> embedder_;
    SearchMetrics metrics_;

    // Configuration
    VectorSearchConfig config_;
};
```

### Graph Search Strategy Implementation

```cpp
class GraphSearchStrategy : public ISearchStrategy {
public:
    GraphSearchStrategy(std::shared_ptr<GraphAnalytics> analytics,
                       std::shared_ptr<EntityResolver> resolver);

    // ISearchStrategy implementation
    SearchResult search(const StructuredQuery& query) override;
    SearchType getStrategyType() const noexcept override { return SearchType::GRAPH; }
    double estimateCost(const StructuredQuery& query) const override;
    bool initialize(const SearchConfiguration& config) override;

    SearchMetrics getMetrics() const override { return metrics_; }
    void resetMetrics() override;
    bool isHealthy() const noexcept override;
    size_t getMemoryUsage() const override;
    void optimizeResources() override;

private:
    // Graph search specific methods
    SearchResult performSearch(const StructuredQuery& query) override;
    void updateMetrics(const SearchResult& result,
                      std::chrono::milliseconds duration) override;

    std::vector<EntityId> findSeedEntities(const StructuredQuery& query) const;
    std::vector<EntityId> expandWithPageRank(
        const std::vector<EntityId>& seeds, int expansion_depth) const;

    // Multi-hop reasoning
    std::vector<RelationshipPath> findReasoningPaths(
        const EntityId& start, const EntityId& end, int max_hops) const;

    // Graph-specific optimizations
    void precomputeCentralityIfNeeded();
    void optimizeTraversalAlgorithms();

    // Member variables
    std::shared_ptr<GraphAnalytics> analytics_;
    std::shared_ptr<EntityResolver> resolver_;
    SearchMetrics metrics_;

    // Cached graph data
    std::unordered_map<EntityId, double> centrality_cache_;
    GraphTraversalAlgorithms algorithms_;

    // Configuration
    GraphSearchConfig config_;
};
```

### Hybrid Fusion Strategy Implementation

```cpp
class HybridSearchStrategy : public ISearchStrategy {
public:
    HybridSearchStrategy(std::shared_ptr<VectorSearchStrategy> vector_strategy,
                        std::shared_ptr<GraphSearchStrategy> graph_strategy,
                        std::shared_ptr<FusionEngine> fusion_engine);

    // ISearchStrategy implementation
    SearchResult search(const StructuredQuery& query) override;
    SearchType getStrategyType() const noexcept override { return SearchType::HYBRID; }
    double estimateCost(const StructuredQuery& query) const override;
    bool initialize(const SearchConfiguration& config) override;

    SearchMetrics getMetrics() const override { return metrics_; }
    void resetMetrics() override;
    bool isHealthy() const noexcept override;
    size_t getMemoryUsage() const override;
    void optimizeResources() override;

private:
    // Hybrid search specific methods
    SearchResult performSearch(const StructuredQuery& query) override;
    void updateMetrics(const SearchResult& result,
                      std::chrono::milliseconds duration) override;

    // Parallel search execution
    struct SearchTask {
        SearchType type;
        StructuredQuery query;
        std::promise<SearchResult> result;
    };

    std::pair<SearchResult, SearchResult> executeParallelSearches(
        const StructuredQuery& query) const;

    // Fusion algorithm
    SearchResult fuseResults(const SearchResult& vector_result,
                            const SearchResult& graph_result) const;

    void calibrateWeights(const StructuredQuery& query);

    // Member variables
    std::shared_ptr<VectorSearchStrategy> vector_strategy_;
    std::shared_ptr<GraphSearchStrategy> graph_strategy_;
    std::shared_ptr<FusionEngine> fusion_engine_;
    SearchMetrics metrics_;

    // Fusion parameters
    float vector_weight_ = 0.6f;
    float graph_weight_ = 0.4f;
    bool adaptive_weighting_ = true;

    // Parallel execution
    mutable std::mutex parallel_execution_mutex_;
    std::vector<std::future<SearchResult>> active_tasks_;
};
```

---

## 🏭 Factory Method Pattern Implementation (Component Creation)

### ComponentFactory Abstract Base

```cpp
class ComponentFactory {
public:
    virtual ~ComponentFactory() = default;

    // Core Factory Methods
    virtual std::unique_ptr<QueryProcessor> createQueryProcessor(
        const QueryProcessorConfig& config) = 0;

    virtual std::unique_ptr<IParsingStrategy> createParser(
        DocumentFormat format, const ParserConfig& config) = 0;

    virtual std::unique_ptr<ISearchStrategy> createSearchStrategy(
        SearchType type, const SearchConfig& config) = 0;

    virtual std::unique_ptr<KnowledgeGraph> createKnowledgeGraph(
        const GraphConfig& config) = 0;

    // Factory Metadata
    virtual std::string getFactoryName() const = 0;
    virtual FactoryCapabilities getCapabilities() const = 0;
    virtual bool supportsComponent(ComponentType type) const = 0;

protected:
    // Helper methods for common factory patterns
    bool validateConfigRequirements(const ComponentConfig& config) const;
    void registerComponentDependencies(ComponentType type,
                                     std::vector<ComponentType> dependencies);
    std::unique_ptr<ComponentMetrics> createMetricsCollector(ComponentType type) const;
};
```

### ProductionFactory Implementation

```cpp
class ProductionFactory : public ComponentFactory {
public:
    // Optimized for performance and reliability
    std::unique_ptr<QueryProcessor> createQueryProcessor(
        const QueryProcessorConfig& config) override {
        return createOptimizedQueryProcessor(config);
    }

    std::unique_ptr<IParsingStrategy> createParser(
        DocumentFormat format, const ParserConfig& config) override {
        return createProductionParser(format, config);
    }

    std::unique_ptr<ISearchStrategy> createSearchStrategy(
        SearchType type, const SearchConfig& config) override {
        return createProductionSearchStrategy(type, config);
    }

    // Production-specific optimizations
    std::unique_ptr<QueryProcessor> createOptimizedQueryProcessor(
        const QueryProcessorConfig& config) {

        // Hardware-specific optimizations
        auto hardware_profile = detectHardwareProfile();

        // Memory pool allocations for high-performance
        auto memory_pool = createApplicationMemoryPool(config.expected_load);

        // Create optimized components
        auto nlp_analyzer = std::make_unique<OptimizedNLPAnalyzer>(config.nlp_config);
        auto intent_predictor = std::make_unique<ProductionIntentPredictor>(
            config.intent_config, hardware_profile);
        auto confidence_scorer = std::make_unique<GPUConfidenceScorer>(
            config.scoring_config, memory_pool);

        // Assembly with performance monitoring
        return std::make_unique<QueryProcessorImpl>(
            std::move(nlp_analyzer),
            std::move(intent_predictor),
            std::move(confidence_scorer),
            memory_pool);
    }

    std::string getFactoryName() const override { return "ProductionFactory"; }
    FactoryCapabilities getCapabilities() const override;
    bool supportsComponent(ComponentType type) const override;
};
```

### TestFactory Implementation

```cpp
class TestFactory : public ComponentFactory {
public:
    // Designed for testing with mocks and controlled scenarios
    std::unique_ptr<QueryProcessor> createQueryProcessor(
        const QueryProcessorConfig& config) override {
        return createTestableQueryProcessor(config);
    }

    std::unique_ptr<IParsingStrategy> createParser(
        DocumentFormat format, const ParserConfig& config) override {
        return createMockParser(format, config);
    }

    std::unique_ptr<ISearchStrategy> createSearchStrategy(
        SearchType type, const SearchConfig& config) override {
        return createControlledSearchStrategy(type, config);
    }

    // Test-specific component creation
    std::unique_ptr<QueryProcessor> createTestableQueryProcessor(
        const QueryProcessorConfig& config) {

        // Create spy/double versions for testing
        auto mock_nlp = std::make_unique<MockNLPAnalyzer>(config.nlp_config);
        auto spy_intent = std::make_unique<SpyIntentPredictor>(config.intent_config);
        auto dummy_scorer = std::make_unique<DummyConfidenceScorer>(config.scoring_config);

        // Controlled memory allocation for tests
        auto test_memory_pool = createTestMemoryPool();

        return std::make_unique<TestQueryProcessorImpl>(
            std::move(mock_nlp),
            std::move(spy_intent),
            std::move(dummy_scorer),
            test_memory_pool);
    }

    std::string getFactoryName() const override { return "TestFactory"; }
    FactoryCapabilities getCapabilities() const override;
    bool supportsComponent(ComponentType type) const override;

    // Test control methods
    void injectTestScenario(const std::string& scenario_name);
    void resetTestState();
    TestScenario getCurrentScenario() const;
};
```

---

## 📨 Message Passing Architecture

### Event-Driven Communication

```cpp
// Event types for component communication
enum class EventType {
    QUERY_RECEIVED,
    QUERY_PROCESSED,
    ENTITIES_EXTRACTED,
    GRAPH_TRAVERSED,
    RESPONSE_GENERATED,
    ERROR_OCCURRED,
    PERFORMANCE_METRIC,
    CONFIGURATION_CHANGED
};

struct SystemEvent {
    EventId id;
    EventType type;
    std::chrono::system_clock::time_point timestamp;
    ComponentId source_component;

    // Event-specific data (variant pattern for type safety)
    std::variant<QueryData, EntityData, GraphData, ResponseData,
                ErrorData, MetricData, ConfigData> payload;

    // Routing information
    EventPriority priority = EventPriority::NORMAL;
    std::vector<ComponentId> target_components;
    bool requires_acknowledgment = false;
};

// Asynchronous event bus
class EventBus {
public:
    using EventHandler = std::function<void(const SystemEvent&)>;

    void publish(const SystemEvent& event);
    SubscriptionId subscribe(EventType type, EventHandler handler,
                           ComponentId subscriber_id);
    void unsubscribe(SubscriptionId id);

private:
    std::unordered_map<EventType, std::vector<std::pair<SubscriptionId, EventHandler>>>
        event_handlers_;

    std::unordered_map<SubscriptionId, EventType> subscription_types_;
    mutable std::shared_mutex handlers_mutex_;

    SubscriptionId generateSubscriptionId();
};
```

### Protocol Contracts

```cpp
// Protocol interface for consistent communication
class ICommunicationProtocol {
public:
    virtual ~ICommunicationProtocol() = default;

    virtual ProtocolType getProtocolType() const = 0;

    // Synchronous communication
    virtual Response sendRequest(const Request& request,
                               std::chrono::milliseconds timeout = 5000ms) = 0;

    // Asynchronous communication
    virtual AsyncRequestHandle sendAsyncRequest(
        const Request& request,
        std::function<void(const Response&)> callback) = 0;

    // Protocol-specific methods
    virtual bool isConnected() const = 0;
    virtual CommunicationStats getStats() const = 0;
    virtual void configure(const ProtocolConfig& config) = 0;
};
```

---

## 🎯 Communication Protocol Benefits

### Observer Pattern Benefits
- **Loose Coupling**: Components communicate through well-defined interfaces
- **Extensibility**: New observers can be added without modifying subjects
- **Real-time Monitoring**: Immediate visibility into system performance
- **Error Isolation**: Observer failures don't affect observed components

### Strategy Pattern Benefits
- **Algorithm Flexibility**: Different search strategies can be swapped dynamically
- **Performance Optimization**: Best algorithm selected per query type
- **Testability**: Each strategy tested independently
- **Scalability**: New algorithms added without changing existing code

### Factory Pattern Benefits
- **Dependency Injection**: Controlled component creation and configuration
- **Environment Adaptation**: Different factories for production/test/benchmarking
- **Lifecycle Management**: Components created with proper initialization
- **Configuration Validation**: Factory ensures component requirements met

---

## 📊 Protocol Performance Characteristics

| **Protocol** | **Latency** | **Throughput** | **Reliability** | **Use Case** |
|--------------|-------------|----------------|-----------------|-------------|
| **Observer** | < 1μs | High (broadcast) | Eventual | Monitoring |
| **Strategy** | < 10μs | Medium (polymorphic) | Synchronous | Flexibility |
| **Factory** | < 100μs | Low (creation) | Synchronous | Construction |
| **Mediator** | < 50μs | Medium (coordination) | Synchronous | Orchestration |
| **Command** | < 20μs | High (batchable) | Synchronous | Workflow |

---

## 🔧 Implementation Notes

### Performance Optimizations
- **Observer Pattern**: Uses weak pointers to prevent circular dependencies
- **Strategy Pattern**: Template specialization for compile-time optimization
- **Factory Pattern**: Pool allocation for frequently created components

### Safety Features
- **Exception Safety**: All protocols designed to not throw exceptions
- **Thread Safety**: Mutex protection where concurrent access possible
- **Resource Limits**: Automatic cleanup of unused connections/subscriptions

### Debugging Support
- **Protocol Tracing**: Optional detailed logging of all communication
- **Metrics Collection**: Comprehensive statistics gathering
- **Error Propagation**: Clear error reporting through defined channels

This communication architecture provides the foundation for reliable, efficient, and maintainable component interactions within the ROMILLM cognitive pipeline.
