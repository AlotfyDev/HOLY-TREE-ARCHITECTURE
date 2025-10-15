#!/usr/bin/env node

/**
 * Graph-RAG MCP Server - Intelligent Knowledge Retrieval and Reasoning
 *
 * Provides cognitive assistance for software development and trading domains
 * through graph-based knowledge representation and hybrid retrieval.
 *
 * Features:
 * - Domain-aware query classification (Software Dev ↔ Trading)
 * - Hybrid vector + graph search with entity reasoning
 * - Cognitive response routing (Deterministic vs Generative)
 * - Multi-modal knowledge integration
 * - Cross-domain relationship mapping
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
  ListPromptsRequestSchema,
  GetPromptRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import * as fs from 'fs';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';
import { winston } from 'winston';
import Database from 'better-sqlite3';
import * as Faiss from 'faiss-node';

// ============================================================================
// TYPE DEFINITIONS
// ============================================================================

/**
 * Domain classification for query routing
 */
enum QueryDomain {
  SOFTWARE_DEVELOPMENT = 'software_dev',
  TRADING_STRATEGY = 'trading_strategy',
  ARCHITECTURAL_DESIGN = 'architecture',
  CROSS_DOMAIN = 'cross_domain',
  GENERAL = 'general'
}

/**
 * Query complexity classification for response strategy
 */
enum QueryComplexity {
  FACTUAL_LOOKUP = 'factual',        // Direct retrieval (fast, accurate)
  STRATEGY_REASONING = 'strategy',   // Algorithmic reasoning (methodical)
  ARCHITECTURAL_ANALYSIS = 'architecture', // System design (holistic)
  COMPARATIVE_ANALYSIS = 'comparative' // Multi-option evaluation
}

/**
 * Response strategy selection
 */
enum ResponseStrategy {
  DETERMINISTIC_RETRIEVAL = 'deterministic',
  GRAPH_REASONING = 'graph_reasoning',
  HYBRID_ANALYSIS = 'hybrid_analysis',
  GENERATIVE_SYNTHESIS = 'generative'
}

/**
 * Knowledge entity representation
 */
interface KnowledgeEntity {
  id: string;
  name: string;
  type: 'concept' | 'pattern' | 'technology' | 'algorithm' | 'design';
  domain: QueryDomain;
  description: string;
  vector: number[];
  relationships: EntityRelationship[];
  metadata: Record<string, any>;
}

/**
 * Entity relationship modeling
 */
interface EntityRelationship {
  targetEntityId: string;
  type: 'related_to' | 'implements' | 'extends' | 'depends_on' | 'compares_to';
  weight: number;        // Relationship strength (0-1)
  context: string;       // Relationship context/description
  domainSpecific: boolean;
}

/**
 * Query context for classification and routing
 */
interface QueryContext {
  rawQuery: string;
  domain: QueryDomain;
  complexity: QueryComplexity;
  strategy: ResponseStrategy;
  entities: string[];
  keywords: string[];
  intent: 'implement' | 'understand' | 'compare' | 'design' | 'debug';
}

/**
 * Hybrid search results
 */
interface HybridSearchResult {
  entity: KnowledgeEntity;
  vectorScore: number;
  graphScore: number;
  combinedScore: number;
  reasoningPath: string[];
  sourceDocuments: string[];
}

/**
 * Cognitive response structure
 */
interface CognitiveResponse {
  answer: string;
  strategy: ResponseStrategy;
  confidence: number;
  entities: KnowledgeEntity[];
  reasoning: string;
  references: Reference[];
  followUpSuggestions: string[];
}

/**
 * Reference with context
 */
interface Reference {
  documentId: string;
  title: string;
  section: string;
  relevanceScore: number;
  excerpt: string;
}

// ============================================================================
// DOMAIN-AWARE QUERY CLASSIFICATION
// ============================================================================

/**
 * Intelligent query classifier that understands development vs trading contexts
 */
class DomainAwareQueryClassifier {
  private softwareKeywords: Set<string> = new Set([
    'function', 'class', 'method', 'api', 'library', 'framework', 'algorithm',
    'data structure', 'design pattern', 'inheritance', 'polymorphism', 'interface',
    'memory', 'performance', 'optimization', 'debugging', 'testing', 'deployment'
  ]);

  private tradingKeywords: Set<string> = new Set([
    'profit', 'loss', 'risk', 'strategy', 'trading', 'market', 'price', 'volume',
    'indicator', 'signal', 'entry', 'exit', 'stop', 'target', 'position', 'leverage',
    'momentum', 'breakout', 'resistance', 'support', 'trend', 'volatility'
  ]);

  private architectureKeywords: Set<string> = new Set([
    'microservices', 'architecture', 'scalability', 'distributed', 'system',
    'design', 'pattern', 'infrastructure', 'cloud', 'deployment', 'monitoring'
  ]);

  classifyQuery(rawQuery: string): QueryContext {
    const query = rawQuery.toLowerCase();
    const words = query.split(/\s+/);

    // Extract entities and keywords
    const entities = this.extractEntities(query);
    const keywords = words.filter(word => word.length > 3);

    // Domain classification
    const domain = this.classifyDomain(query);

    // Complexity analysis
    const complexity = this.analyzeComplexity(query, domain);

    // Intent classification
    const intent = this.classifyIntent(query);

    // Strategy selection
    const strategy = this.selectStrategy(domain, complexity, intent);

    return {
      rawQuery,
      domain,
      complexity,
      strategy,
      entities,
      keywords,
      intent
    };
  }

  private classifyDomain(query: string): QueryDomain {
    const softwareScore = this.scoreKeywords(query, this.softwareKeywords);
    const tradingScore = this.scoreKeywords(query, this.tradingKeywords);
    const architectureScore = this.scoreKeywords(query, this.architectureKeywords);

    // Cross-domain indicators
    const crossDomainIndicators = ['compare', 'versus', 'vs', 'alternative', 'approach'];

    if (crossDomainIndicators.some(indicator => query.includes(indicator))) {
      return QueryDomain.CROSS_DOMAIN;
    }

    // Score-based classification
    if (softwareScore > tradingScore && softwareScore > architectureScore) {
      return QueryDomain.SOFTWARE_DEVELOPMENT;
    } else if (tradingScore > softwareScore) {
      return QueryDomain.TRADING_STRATEGY;
    } else if (architectureScore > 0) {
      return QueryDomain.ARCHITECTURAL_DESIGN;
    }

    return QueryDomain.GENERAL;
  }

  private analyzeComplexity(query: string, domain: QueryDomain): QueryComplexity {
    const complexityIndicators = {
      [QueryComplexity.FACTUAL_LOOKUP]: ['what is', 'how to', 'definition', 'explain', 'meaning'],
      [QueryComplexity.STRATEGY_REASONING]: ['strategy', 'approach', 'method', 'technique', 'algorithm'],
      [QueryComplexity.ARCHITECTURAL_ANALYSIS]: ['architecture', 'system', 'design', 'infrastructure', 'scalability'],
      [QueryComplexity.COMPARATIVE_ANALYSIS]: ['compare', 'versus', 'better', 'advantage', 'trade-off', 'alternative']
    };

    for (const [complexity, indicators] of Object.entries(complexityIndicators)) {
      if (indicators.some(indicator => query.includes(indicator))) {
        return complexity as QueryComplexity;
      }
    }

    // Domain-specific defaults
    switch (domain) {
      case QueryDomain.SOFTWARE_DEVELOPMENT:
        return QueryComplexity.FACTUAL_LOOKUP;
      case QueryDomain.TRADING_STRATEGY:
        return QueryComplexity.STRATEGY_REASONING;
      case QueryDomain.ARCHITECTURAL_DESIGN:
        return QueryComplexity.ARCHITECTURAL_ANALYSIS;
      default:
        return QueryComplexity.FACTUAL_LOOKUP;
    }
  }

  private classifyIntent(query: string): 'implement' | 'understand' | 'compare' | 'design' | 'debug' {
    if (query.includes('implement') || query.includes('code') || query.includes('example')) {
      return 'implement';
    } else if (query.includes('understand') || query.includes('explain') || query.includes('meaning')) {
      return 'understand';
    } else if (query.includes('compare') || query.includes('versus') || query.includes('better')) {
      return 'compare';
    } else if (query.includes('design') || query.includes('architecture') || query.includes('system')) {
      return 'design';
    } else if (query.includes('debug') || query.includes('error') || query.includes('problem')) {
      return 'debug';
    }

    return 'understand'; // Default intent
  }

  private selectStrategy(domain: QueryDomain, complexity: QueryComplexity, intent: string): ResponseStrategy {
    // Strategy selection matrix
    if (domain === QueryDomain.SOFTWARE_DEVELOPMENT && complexity === QueryComplexity.FACTUAL_LOOKUP) {
      return ResponseStrategy.DETERMINISTIC_RETRIEVAL;
    } else if (domain === QueryDomain.TRADING_STRATEGY) {
      return ResponseStrategy.GRAPH_REASONING;
    } else if (complexity === QueryComplexity.COMPARATIVE_ANALYSIS) {
      return ResponseStrategy.HYBRID_ANALYSIS;
    } else if (domain === QueryDomain.ARCHITECTURAL_DESIGN) {
      return ResponseStrategy.GENERATIVE_SYNTHESIS;
    }

    return ResponseStrategy.HYBRID_ANALYSIS; // Safe default
  }

  private scoreKeywords(query: string, keywords: Set<string>): number {
    return Array.from(keywords).reduce((score, keyword) => {
      return score + (query.split(keyword).length - 1);
    }, 0);
  }

  private extractEntities(query: string): string[] {
    // Extract potential entity names from query
    const words = query.split(/\s+/);
    return words.filter(word =>
      word.length > 3 &&
      !this.isStopWord(word) &&
      word.match(/^[a-zA-Z][a-zA-Z0-9_]*$/)
    );
  }

  private isStopWord(word: string): boolean {
    const stopWords = new Set(['what', 'how', 'why', 'when', 'where', 'which', 'with', 'from', 'into', 'this', 'that', 'then', 'than']);
    return stopWords.has(word.toLowerCase());
  }
}

// ============================================================================
// HYBRID RETRIEVAL ENGINE
// ============================================================================

/**
 * Intelligent retrieval combining vector similarity and graph reasoning
 */
class HybridRetrievalEngine {
  private db: Database.Database;
  private vectorIndex: Faiss.Index;
  private logger: winston.Logger;

  constructor(knowledgeBasePath: string) {
    this.db = new Database(path.join(knowledgeBasePath, 'knowledge.db'));
    this.vectorIndex = new Faiss.IndexFlat();
    this.setupDatabase();

    // Setup logging
    this.logger = winston.createLogger({
      level: 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json()
      ),
      transports: [
        new winston.transports.File({ filename: path.join(knowledgeBasePath, 'retrieval.log') })
      ]
    });
  }

  /**
   * Hybrid search with domain calibration
   */
  async hybridSearch(query: QueryContext, topK: number = 10): Promise<HybridSearchResult[]> {
    this.logger.info('Starting hybrid search', { query: query.rawQuery, domain: query.domain });

    // Parallel vector + graph search
    const [vectorResults, graphResults] = await Promise.all([
      this.vectorSearch(query, topK),
      this.graphSearch(query, topK)
    ]);

    // Domain-aware fusion
    return this.fuseResults(vectorResults, graphResults, query);
  }

  private async vectorSearch(query: QueryContext, topK: number): Promise<KnowledgeEntity[]> {
    // Convert query to embedding (placeholder - would use actual model)
    const queryVector = await this.embedQuery(query.rawQuery);

    // Search vector index
    const { distances, indices } = this.vectorIndex.search(queryVector, topK);

    // Retrieve entities from database
    const entities: KnowledgeEntity[] = [];
    const stmt = this.db.prepare('SELECT * FROM entities WHERE id = ?');

    for (const idx of indices) {
      if (idx >= 0) {
        const row = stmt.get(idx.toString());
        if (row) {
          entities.push(JSON.parse(row.data));
        }
      }
    }

    return entities;
  }

  private async graphSearch(query: QueryContext, topK: number): Promise<KnowledgeEntity[]> {
    // Find entities mentioned in query
    const entityMatches = await this.findNamedEntities(query.entities);

    // Graph traversal from matched entities
    const exploredEntities = new Set<string>();
    const relevantEntities: KnowledgeEntity[] = [];

    for (const entity of entityMatches) {
      await this.traverseGraph(entity, exploredEntities, relevantEntities, query, 2); // 2-hop traversal
    }

    return relevantEntities.slice(0, topK);
  }

  private async traverseGraph(
    currentEntity: KnowledgeEntity,
    explored: Set<string>,
    relevant: KnowledgeEntity[],
    query: QueryContext,
    depth: number
  ): Promise<void> {
    if (explored.has(currentEntity.id) || depth <= 0) return;
    explored.add(currentEntity.id);

    // Check relevance to query
    if (this.isRelevantToQuery(currentEntity, query)) {
      relevant.push(currentEntity);
    }

    // Traverse relationships
    const stmt = this.db.prepare(`
      SELECT target_entity_id, relationship_type, weight
      FROM relationships
      WHERE source_entity_id = ?
      AND weight > 0.3
      ORDER BY weight DESC
      LIMIT 5
    `);

    const relationships = stmt.all(currentEntity.id);
    for (const rel of relationships) {
      const targetEntity = await this.loadEntity(rel.target_entity_id);
      if (targetEntity) {
        await this.traverseGraph(targetEntity, explored, relevant, query, depth - 1);
      }
    }
  }

  private fuseResults(
    vectorResults: KnowledgeEntity[],
    graphResults: KnowledgeEntity[],
    query: QueryContext
  ): HybridSearchResult[] {
    const resultMap = new Map<string, HybridSearchResult>();

    // Process vector results
    vectorResults.forEach((entity, index) => {
      resultMap.set(entity.id, {
        entity,
        vectorScore: 1.0 - (index * 0.1), // Decay with rank
        graphScore: 0.0,
        combinedScore: 0.0,
        reasoningPath: [],
        sourceDocuments: []
      });
    });

    // Process graph results
    graphResults.forEach(entity => {
      const existing = resultMap.get(entity.id);
      if (existing) {
        existing.graphScore = 0.8;
      } else {
        resultMap.set(entity.id, {
          entity,
          vectorScore: 0.0,
          graphScore: 0.8,
          combinedScore: 0.0,
          reasoningPath: [],
          sourceDocuments: []
        });
      }
    });

    // Calculate domain-calibrated combined scores
    const weights = this.getDomainWeights(query);
    const results: HybridSearchResult[] = [];

    for (const result of resultMap.values()) {
      result.combinedScore = result.vectorScore * weights.vector + result.graphScore * weights.graph;
      results.push(result);
    }

    // Sort by combined score
    results.sort((a, b) => b.combinedScore - a.combinedScore);
    return results.slice(0, 10);
  }

  private getDomainWeights(query: QueryContext): { vector: number; graph: number } {
    // Domain-specific fusion weights
    switch (query.domain) {
      case QueryDomain.SOFTWARE_DEVELOPMENT:
        return { vector: 0.7, graph: 0.3 }; // Favor vector for factual lookups
      case QueryDomain.TRADING_STRATEGY:
        return { vector: 0.4, graph: 0.6 }; // Favor graph for strategy relationships
      case QueryDomain.ARCHITECTURAL_DESIGN:
        return { vector: 0.5, graph: 0.5 }; // Balanced for design reasoning
      default:
        return { vector: 0.6, graph: 0.4 }; // Default balance
    }
  }

  private isRelevantToQuery(entity: KnowledgeEntity, query: QueryContext): boolean {
    // Domain-specific relevance checking
    if (entity.domain !== query.domain && query.domain !== QueryDomain.CROSS_DOMAIN) {
      return false;
    }

    // Keyword matching
    const entityText = (entity.name + ' ' + entity.description).toLowerCase();
    return query.keywords.some(keyword => entityText.includes(keyword.toLowerCase()));
  }

  private async findNamedEntities(names: string[]): Promise<KnowledgeEntity[]> {
    const entities: KnowledgeEntity[] = [];
    const stmt = this.db.prepare('SELECT data FROM entities WHERE name LIKE ?');

    for (const name of names) {
      const rows = stmt.all(`%${name}%`);
      for (const row of rows) {
        entities.push(JSON.parse(row.data));
      }
    }

    return entities;
  }

  private async loadEntity(entityId: string): Promise<KnowledgeEntity | null> {
    const stmt = this.db.prepare('SELECT data FROM entities WHERE id = ?');
    const row = stmt.get(entityId);
    return row ? JSON.parse(row.data) : null;
  }

  private async embedQuery(query: string): Promise<number[]> {
    // Placeholder - would use actual embedding model
    // For now, return normalized random vector
    return Array.from({ length: 384 }, () => Math.random()).map(x => x / Math.sqrt(384));
  }

  private setupDatabase(): void {
    // Create tables for knowledge graph
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS entities (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        data TEXT NOT NULL
      );

      CREATE TABLE IF NOT EXISTS relationships (
        id TEXT PRIMARY KEY,
        source_entity_id TEXT NOT NULL,
        target_entity_id TEXT NOT NULL,
        relationship_type TEXT NOT NULL,
        weight REAL DEFAULT 1.0,
        context TEXT,
        domain_specific BOOLEAN DEFAULT FALSE,
        FOREIGN KEY(source_entity_id) REFERENCES entities(id),
        FOREIGN KEY(target_entity_id) REFERENCES entities(id)
      );

      CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        domain TEXT,
        last_modified DATETIME DEFAULT CURRENT_TIMESTAMP
      );

      CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name);
      CREATE INDEX IF NOT EXISTS idx_relationships_source ON relationships(source_entity_id);
      CREATE INDEX IF NOT EXISTS idx_relationships_target ON relationships(target_entity_id);
    `);
  }
}

// ============================================================================
// COGNITIVE RESPONSE SYSTEM
// ============================================================================

/**
 * Intelligent response generation with strategy selection
 */
class CognitiveResponseGenerator {
  private classifier: DomainAwareQueryClassifier;
  private retrieval: HybridRetrievalEngine;
  private logger: winston.Logger;

  constructor(retrieval: HybridRetrievalEngine, knowledgePath: string) {
    this.classifier = new DomainAwareQueryClassifier();
    this.retrieval = retrieval;

    this.logger = winston.createLogger({
      level: 'info',
      transports: [
        new winston.transports.File({ filename: path.join(knowledgePath, 'responses.log') })
      ]
    });
  }

  async generateResponse(query: string, context?: any): Promise<CognitiveResponse> {
    const startTime = Date.now();

    // Classify query and determine strategy
    const queryContext = this.classifier.classifyQuery(query);
    this.logger.info('Query classified', {
      query: query.slice(0, 100),
      domain: queryContext.domain,
      complexity: queryContext.complexity,
      strategy: queryContext.strategy
    });

    // Execute hybrid retrieval
    const searchResults = await this.retrieval.hybridSearch(queryContext);

    // Generate response based on strategy
    const response = await this.executeStrategy(queryContext, searchResults);

    const processingTime = Date.now() - startTime;
    this.logger.info('Response generated', {
      processingTime,
      entitiesReturned: response.entities.length,
      strategy: response.strategy,
      confidence: response.confidence
    });

    return response;
  }

  private async executeStrategy(
    context: QueryContext,
    results: HybridSearchResult[]
  ): Promise<CognitiveResponse> {
    switch (context.strategy) {
      case ResponseStrategy.DETERMINISTIC_RETRIEVAL:
        return this.deterministicRetrieval(context, results);

      case ResponseStrategy.GRAPH_REASONING:
        return this.graphReasoning(context, results);

      case ResponseStrategy.HYBRID_ANALYSIS:
        return this.hybridAnalysis(context, results);

      case ResponseStrategy.GENERATIVE_SYNTHESIS:
        return this.generativeSynthesis(context, results);

      default:
        return this.fallbackResponse(context, results);
    }
  }

  private deterministicRetrieval(context: QueryContext, results: HybridSearchResult[]): CognitiveResponse {
    // For factual queries, provide direct, authoritative answers
    const topResult = results[0];
    if (!topResult) {
      return this.noResultsResponse(context);
    }

    const answer = this.formatDirectAnswer(topResult.entity, context);

    return {
      answer,
      strategy: ResponseStrategy.DETERMINISTIC_RETRIEVAL,
      confidence: topResult.combinedScore,
      entities: [topResult.entity],
      reasoning: "Direct factual retrieval from knowledge base",
      references: [{
        documentId: 'kb_001',
        title: 'Knowledge Base',
        section: topResult.entity.type,
        relevanceScore: topResult.combinedScore,
        excerpt: topResult.entity.description
      }],
      followUpSuggestions: this.generateFollowUps(context, 'factual')
    };
  }

  private graphReasoning(context: QueryContext, results: HybridSearchResult[]): CognitiveResponse {
    // For strategy/reasoning queries, weave together relationships
    const primaryEntity = results[0]?.entity;
    const relatedEntities = results.slice(1, 4).map(r => r.entity);

    const reasoning = this.buildReasoningChain(primaryEntity, relatedEntities, context);
    const answer = this.formatReasonedResponse(reasoning, context);

    return {
      answer,
      strategy: ResponseStrategy.GRAPH_REASONING,
      confidence: results[0]?.combinedScore || 0.5,
      entities: results.map(r => r.entity),
      reasoning: "Graph-based reasoning through entity relationships",
      references: results.map((result, index) => ({
        documentId: `entity_${index}`,
        title: result.entity.name,
        section: result.entity.type,
        relevanceScore: result.combinedScore,
        excerpt: result.entity.description
      })),
      followUpSuggestions: this.generateFollowUps(context, 'reasoning')
    };
  }

  private hybridAnalysis(context: QueryContext, results: HybridSearchResult[]): CognitiveResponse {
    // For comparative/analytical queries
    const analysis = this.performComparativeAnalysis(results, context);

    return {
      answer: analysis.summary,
      strategy: ResponseStrategy.HYBRID_ANALYSIS,
      confidence: this.calculateAnalysisConfidence(results),
      entities: results.map(r => r.entity),
      reasoning: analysis.methodology,
      references: analysis.evidence,
      followUpSuggestions: this.generateFollowUps(context, 'analysis')
    };
  }

  private generativeSynthesis(context: QueryContext, results: HybridSearchResult[]): CognitiveResponse {
    // For complex design/architecture questions requiring synthesis
    // Note: In real implementation, this would call an LLM
    const synthesis = this.generateSyntheticResponse(results, context);

    return {
      answer: synthesis.response,
      strategy: ResponseStrategy.GENERATIVE_SYNTHESIS,
      confidence: synthesis.confidence,
      entities: results.map(r => r.entity),
      reasoning: "Synthesized response from multiple knowledge sources",
      references: synthesis.references,
      followUpSuggestions: this.generateFollowUps(context, 'synthesis')
    };
  }

  private fallbackResponse(context: QueryContext, results: HybridSearchResult[]): CognitiveResponse {
    return {
      answer: "Based on the available knowledge, here's what I found relevant to your query...",
      strategy: ResponseStrategy.DETERMINISTIC_RETRIEVAL,
      confidence: 0.3,
      entities: results.slice(0, 3).map(r => r.entity),
      reasoning: "Fallback response due to unclear query classification",
      references: [],
      followUpSuggestions: ["Try being more specific about your question", "Provide more context about the domain"]
    };
  }

  private noResultsResponse(context: QueryContext): CognitiveResponse {
    return {
      answer: "I couldn't find specific information about that query in the knowledge base.",
      strategy: ResponseStrategy.DETERMINISTIC_RETRIEVAL,
      confidence: 0.0,
      entities: [],
      reasoning: "No matching entities found in knowledge base",
      references: [],
      followUpSuggestions: [
        "Try rephrasing your question",
        `Consider that this might be domain-specific (${context.domain})`,
        "Try a more general or related query"
      ]
    };
  }

  private formatDirectAnswer(entity: KnowledgeEntity, context: QueryContext): string {
    return `**${entity.name}**

${entity.description}

${this.formatEntityDetails(entity)}`;
  }

  private formatEntityDetails(entity: KnowledgeEntity): string {
    const details = [];
    if (entity.relationships.length > 0) {
      details.push(`**Related Concepts:** ${entity.relationships.slice(0, 3).map(r => r.context).join(', ')}`);
    }

    if (entity.metadata.examples) {
      details.push(`**Examples:** ${entity.metadata.examples.join(', ')}`);
    }

    return details.join('\n\n');
  }

  private buildReasoningChain(primary: KnowledgeEntity | undefined, related: KnowledgeEntity[], context: QueryContext): any {
    if (!primary) return null;

    return {
      primary: primary.name,
      reasoning: `Starting from ${primary.name} (${primary.type}), related concepts include: ${related.map(e => e.name).join(', ')}. This suggests a ${context.intent} approach.`,
      steps: [
        `Identify core concept: ${primary.name}`,
        `Find related techniques: ${related.map(e => e.name).join(', ')}`,
        `Determine appropriate strategy for ${context.domain} domain`
      ]
    };
  }

  private formatReasonedResponse(reasoning: any, context: QueryContext): string {
    if (!reasoning) return "Unable to construct reasoning chain from available information.";

    return `## Recommended ${context.intent.charAt(0).toUpperCase() + context.intent.slice(1)} Approach

**${reasoning.reasoning}**

### Step-by-Step Reasoning:
${reasoning.steps.map((step: string, i: number) => `${i + 1}. ${step}`).join('\n')}

### Related Concepts:
${reasoning.primary} connects to broader patterns in ${context.domain} development.`;
  }

  private performComparativeAnalysis(results: HybridSearchResult[], context: QueryContext): any {
    const entities = results.map(r => r.entity);
    const summary = `## Comparative Analysis of ${context.intent} Options

Examining ${entities.length} approaches for ${context.rawQuery}:

${entities.map((entity, i) => `**${i + 1}. ${entity.name}:** ${entity.description.slice(0, 100)}...`).join('\n\n')}

### Key Trade-offs:`;

    return {
      summary,
      methodology: "Comparative analysis across multiple knowledge entities",
      evidence: entities.map(entity => ({
        documentId: entity.id,
        title: entity.name,
        section: entity.type,
        relevanceScore: 1.0,
        excerpt: entity.description
      }))
    };
  }

  private calculateAnalysisConfidence(results: HybridSearchResult[]): number {
    if (results.length === 0) return 0.0;
    return results.reduce((sum, r) => sum + r.combinedScore, 0) / results.length;
  }

  private generateSyntheticResponse(results: HybridSearchResult[], context: QueryContext): any {
    // Placeholder for LLM synthesis (would integrate actual model)
    const response = `## Synthesized Solution for ${context.rawQuery}

Drawing from ${results.length} knowledge sources in ${context.domain}:

${results.map(r => `- **${r.entity.name}:** ${r.entity.description}`).join('\n')}

### Integrated Approach:
Combining insights from ${context.domain} knowledge base to provide a comprehensive solution.`;

    return {
      response,
      confidence: 0.7,
      references: results.map(r => ({
        documentId: r.entity.id,
        title: r.entity.name,
        section: r.entity.type,
        relevanceScore: r.combinedScore,
        excerpt: r.entity.description
      }))
    };
  }

  private generateFollowUps(context: QueryContext, responseType: string): string[] {
    const suggestions = [];

    switch (responseType) {
      case 'factual':
        suggestions.push(`Would you like implementation examples for ${context.entities.join(', ')}?`);
        suggestions.push("Need to see usage patterns or best practices?");
        break;

      case 'reasoning':
        suggestions.push("Want to explore alternative approaches?");
        suggestions.push("Need performance considerations or trade-offs explained?");
        break;

      case 'analysis':
        suggestions.push("Want to dive deeper into any specific option?");
        suggestions.push("Need implementation details or code examples?");
        break;
    }

    return suggestions;
  }
}

// ============================================================================
// MCP SERVER IMPLEMENTATION
// ============================================================================

/**
 * Main MCP Server for Graph-RAG Cognitive Assistance
 */
class GraphRagMcpServer {
  private classifier: DomainAwareQueryClassifier;
  private retrieval: HybridRetrievalEngine;
  private responseGenerator: CognitiveResponseGenerator;
  private server: Server;

  constructor(knowledgeBasePath: string = './knowledge-base') {
    // Ensure knowledge base directory exists
    if (!fs.existsSync(knowledgeBasePath)) {
      fs.mkdirSync(knowledgeBasePath, { recursive: true });
    }

    this.classifier = new DomainAwareQueryClassifier();
    this.retrieval = new HybridRetrievalEngine(knowledgeBasePath);
    this.responseGenerator = new CognitiveResponseGenerator(this.retrieval, knowledgeBasePath);

    this.server = new Server(
      {
        name: "GraphRAG-CognitiveAssistant",
        version: "1.0.0"
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupServerHandlers();
  }

  private setupServerHandlers(): void {
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: "query_software_documentation",
            description: "Query software development knowledge with code examples and best practices from documentation and codebase insights",
            inputSchema: {
              type: "object",
              properties: {
                query: {
                  type: "string",
                  description: "Natural language question about software development"
                },
                context: {
                  type: "object",
                  properties: {
                    project_type: {
                      type: "string",
                      description: "Project context (e.g., 'C++_GUI_Application', 'Python_ML_Project')"
                    },
                    programming_languages: {
                      type: "array",
                      items: { type: "string" },
                      description: "Preferred programming languages"
                    },
                    response_style: {
                      type: "string",
                      enum: ["code_examples", "theoretical", "practical_guide", "comparison"],
                      description: "Preferred response style"
                    }
                  }
                }
              },
              required: ["query"]
            }
          },
          {
            name: "reason_algorithmic_strategy",
            description: "Deep reasoning about algorithmic strategies, combining trading knowledge with software implementation approaches",
            inputSchema: {
              type: "object",
              properties: {
                query: {
                  type: "string",
                  description: "Question about algorithmic strategies or trading approaches"
                },
                constraints: {
                  type: "object",
                  properties: {
                    risk_level: { type: "string", enum: ["conservative", "moderate", "aggressive"] },
                    time_horizon: { type: "string", enum: ["short", "medium", "long"] },
                    implementation_complexity: { type: "string", enum: ["simple", "moderate", "advanced"] }
                  }
                },
                focus_areas: {
                  type: "array",
                  items: { type: "string" },
                  description: "Specific areas to focus on (e.g., 'entry_signals', 'risk_management')"
                }
              },
              required: ["query"]
            }
          },
          {
            name: "analyze_architecture_patterns",
            description: "Architectural analysis and design recommendations with cross-domain insights from software systems and trading platforms",
            inputSchema: {
              type: "object",
              properties: {
                query: {
                  type: "string",
                  description: "Architecture or system design question"
                },
                constraints: {
                  type: "object",
                  properties: {
                    scale: { type: "string", enum: ["small", "medium", "large", "enterprise"] },
                    performance_requirements: { type: "string", enum: ["high_performance", "balanced", "cost_optimized"] },
                    technology_stack: { type: "array", items: { type: "string" } }
                  }
                }
              },
              required: ["query"]
            }
          },
          {
            name: "compare_technology_options",
            description: "Comparative analysis of technological approaches, frameworks, or design patterns with evidence-based recommendations",
            inputSchema: {
              type: "object",
              properties: {
                query: {
                  type: "string",
                  description: "Comparison question (e.g., 'React vs Vue', 'REST vs GraphQL')"
                },
                evaluation_criteria: {
                  type: "array",
                  items: { type: "string" },
                  description: "Criteria for comparison (e.g., 'performance', 'developer_experience', 'scalability')"
                },
                context_domain: {
                  type: "string",
                  description: "Domain context for evaluation (e.g., 'web_development', 'data_processing')"
                }
              },
              required: ["query", "evaluation_criteria"]
            }
          },
          {
            name: "explain_concept_relationships",
            description: "Explain how concepts relate across domains, providing contextual understanding and practical connections",
            inputSchema: {
              type: "object",
              properties: {
                concept: {
                  type: "string",
                  description: "Primary concept to explain"
                },
                related_entities: {
                  type: "array",
                  items: { type: "string" },
                  description: "Related concepts or technologies"
                },
                explanation_depth: {
                  type: "string",
                  enum: ["basic", "intermediate", "advanced"],
                  description: "Desired explanation depth"
                },
                application_context: {
                  type: "string",
                  description: "How the concept applies in practice"
                }
              },
              required: ["concept", "related_entities"]
            }
          }
        ]
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case "query_software_documentation":
            return await this.handleSoftwareDocumentationQuery(args?.query, args?.context);

          case "reason_algorithmic_strategy":
            return await this.handleAlgorithmicStrategyQuery(args?.query, args?.constraints, args?.focus_areas);

          case "analyze_architecture_patterns":
            return await this.handleArchitectureAnalysis(args?.query, args?.constraints);

          case "compare_technology_options":
            return await this.handleTechnologyComparison(args?.query, args?.evaluation_criteria, args?.context_domain);

          case "explain_concept_relationships":
            return await this.handleConceptRelationships(args?.concept, args?.related_entities, args?.explanation_depth, args?.application_context);

          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      } catch (error) {
        throw new Error(`Tool execution failed: ${(error as Error).message}`);
      }
    });
  }

  private async handleSoftwareDocumentationQuery(query: string, context?: any) {
    const enhancedQuery = this.enhanceSoftwareQuery(query, context);
    const response = await this.responseGenerator.generateResponse(enhancedQuery);

    return {
      content: [{
        type: "text",
        text: this.formatMarkdownResponse(response)
      }]
    };
  }

  private async handleAlgorithmicStrategyQuery(query: string, constraints?: any, focusAreas?: string[]) {
    const enhancedQuery = this.enhanceStrategyQuery(query, constraints, focusAreas);
    const response = await this.responseGenerator.generateResponse(enhancedQuery);

    return {
      content: [{
        type: "text",
        text: this.formatMarkdownResponse(response)
      }]
    };
  }

  private async handleArchitectureAnalysis(query: string, constraints?: any) {
    const enhancedQuery = this.enhanceArchitectureQuery(query, constraints);
    const response = await this.responseGenerator.generateResponse(enhancedQuery);

    return {
      content: [{
        type: "text",
        text: this.formatMarkdownResponse(response)
      }]
    };
  }

  private async handleTechnologyComparison(query: string, criteria: string[], domain?: string) {
    const enhancedQuery = this.enhanceComparisonQuery(query, criteria, domain);
    const response = await this.responseGenerator.generateResponse(enhancedQuery);

    return {
      content: [{
        type: "text",
        text: this.formatMarkdownResponse(response)
      }]
    };
  }

  private async handleConceptRelationships(concept: string, entities: string[], depth?: string, context?: string) {
    const enhancedQuery = `Explain how ${concept} relates to ${entities.join(', ')} in ${depth || 'intermediate'} depth. ${context ? `Context: ${context}` : ''}`;
    const response = await this.responseGenerator.generateResponse(enhancedQuery);

    return {
      content: [{
        type: "text",
        text: this.formatMarkdownResponse(response)
      }]
    };
  }

  private enhanceSoftwareQuery(query: string, context?: any): string {
    let enhanced = query;

    if (context?.project_type) {
      enhanced += ` in the context of a ${context.project_type}`;
    }

    if (context?.programming_languages?.length > 0) {
      enhanced += ` with focus on ${context.programming_languages.join(', ')}`;
    }

    if (context?.response_style === 'code_examples') {
      enhanced += '. Provide practical code examples and implementation guidance';
    } else if (context?.response_style === 'theoretical') {
      enhanced += '. Focus on theoretical understanding and concepts';
    }

    return enhanced;
  }

  private enhanceStrategyQuery(query: string, constraints?: any, focusAreas?: string[]): string {
    let enhanced = query;

    if (constraints?.risk_level) {
      enhanced += ` considering ${constraints.risk_level} risk tolerance`;
    }

    if (constraints?.time_horizon) {
      enhanced += ` for ${constraints.time_horizon}-term trading`;
    }

    if (focusAreas?.length > 0) {
      enhanced += `. Focus on: ${focusAreas.join(', ')}`;
    }

    enhanced += '. Include algorithmic implementation considerations';

    return enhanced;
  }

  private enhanceArchitectureQuery(query: string, constraints?: any): string {
    let enhanced = query;

    if (constraints?.scale) {
      enhanced += ` for a ${constraints.scale}-scale system`;
    }

    if (constraints?.performance_requirements) {
      enhanced += ` with ${constraints.performance_requirements} requirements`;
    }

    if (constraints?.technology_stack?.length > 0) {
      enhanced += ` using ${constraints.technology_stack.join(', ')}`;
    }

    enhanced += '. Include architectural patterns and trade-offs analysis';

    return enhanced;
  }

  private enhanceComparisonQuery(query: string, criteria: string[], domain?: string): string {
    let enhanced = `${query}. Evaluate based on: ${criteria.join(', ')}`;

    if (domain) {
      enhanced += ` in the context of ${domain}`;
    }

    enhanced += '. Provide evidence-based comparison with practical recommendations';

    return enhanced;
  }

  private formatMarkdownResponse(response: CognitiveResponse): string {
    let markdown = `${response.answer}\n\n`;

    // Add confidence indicator
    const confidenceLevel = response.confidence > 0.8 ? 'High' :
                           response.confidence > 0.6 ? 'Medium' : 'Low';
    markdown += `**Confidence:** ${confidenceLevel} (${Math.round(response.confidence * 100)}%)\n\n`;

    // Add reasoning
    if (response.reasoning) {
      markdown += `**Reasoning:** ${response.reasoning}\n\n`;
    }

    // Add references
    if (response.references.length > 0) {
      markdown += `**References:**\n`;
      response.references.forEach((ref, i) => {
        markdown += `${i + 1}. **${ref.title}** (${ref.relevanceScore.toFixed(2)} relevance)\n`;
        if (ref.excerpt) {
          markdown += `   "${ref.excerpt.slice(0, 100)}${ref.excerpt.length > 100 ? '...' : ''}"\n`;
        }
      });
      markdown += '\n';
    }

    // Add follow-up suggestions
    if (response.followUpSuggestions.length > 0) {
      markdown += `**Suggestions:**\n`;
      response.followUpSuggestions.forEach(suggestion => {
        markdown += `• ${suggestion}\n`;
      });
    }

    return markdown;
  }

  async start(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error("Graph-RAG Cognitive Assistant MCP Server running on stdio");
  }
}

// ============================================================================
// MAIN EXECUTION
// ============================================================================

async function main() {
  const knowledgeBasePath = process.env.KNOWLEDGE_BASE_PATH || './knowledge-base';
  const server = new GraphRagMcpServer(knowledgeBasePath);

  await server.start();
}

main().catch((error) => {
  console.error("Graph-RAG MCP Server error:", error);
  process.exit(1);
});
