package amqp.spring.camel.component;
import org.apache.camel.Consumer;
import org.apache.camel.Processor;
import org.apache.camel.Producer;
import org.apache.camel.impl.DefaultEndpoint;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.core.AmqpAdmin;
import org.springframework.amqp.core.AmqpTemplate;
import org.springframework.amqp.core.DirectExchange;
import org.springframework.amqp.core.FanoutExchange;
import org.springframework.amqp.core.HeadersExchange;
import org.springframework.amqp.core.TopicExchange;

/**
 * RabbitMQ Consumer URIs are in the format of:<br/>
 * <code>spring-amqp:exchange:queue:routingKey?params=values</code><br/>
 * 
 * RabbitMQ Producer URIs are in the format of:<br/>
 * <code>spring-amqp:exchange:routingKey?params=values</code><br/>
 * 
 * Producers can also defer the routing key to the message header, in which case the URI could be:<br/>
 * <code>spring-amqp:exchange?params=values</code><br/>
 * And the ROUTING_KEY header could be set to the appropriate routing key.
 */
public class SpringAMQPEndpoint extends DefaultEndpoint {
  private static transient final Logger LOG = LoggerFactory.getLogger(SpringAMQPEndpoint.class);

  protected AmqpAdmin amqpAdministration;


<<<<<<< merge_dirs/Bluelock/camel-spring-amqp/c31678d8644cd608d2b55d4f3e8c28c103c9604c/SpringAMQPEndpoint.java_b3dc5b056c73548c458ba0a6e581102d878c2a6c/Left.java
  long idleThreadKeepAliveMillis = 60000;
=======
  private static final String DEFAULT_EXCHANGE_NAME = "";
>>>>>>> merge_dirs/Bluelock/camel-spring-amqp/c31678d8644cd608d2b55d4f3e8c28c103c9604c/SpringAMQPEndpoint.java_b3dc5b056c73548c458ba0a6e581102d878c2a6c/Right.java


  protected AmqpTemplate amqpTemplate;

  String exchangeName;

  String queueName;

  String routingKey;

  String exchangeType;

  boolean durable = false;

  boolean exclusive = false;

  boolean autodelete = true;

  boolean transactional = false;

  int concurrentConsumers = 1;

  int prefetchCount = 1;

  Integer timeToLive = null;

  long idleThreadKeepAliveMillis = 60000;

  int threadPoolIdleSize = 4;

  int threadPoolMaxSize = 20;

  private String tempQueueOrKey;

  public SpringAMQPEndpoint(String remaining, AmqpTemplate template, AmqpAdmin admin) {
    LOG.info("Creating endpoint for {}", remaining);
    this.amqpAdministration = admin;
    this.amqpTemplate = template;
    String[] tokens = remaining.split(":");
    this.exchangeName = tokens.length == 0 || tokens[0] == null ? "" : tokens[0];
    if (tokens.length > 2) {
      this.queueName = tokens[1];
      this.routingKey = tokens[2];
    } else {
      if (tokens.length == 2) {
        this.tempQueueOrKey = tokens[1];
      } else {
        this.exchangeType = "fanout";
      }
    }
  }

  @Override public Producer createProducer() throws Exception {
    if (this.exchangeName == null) {
      throw new IllegalStateException("Cannot have null exchange name");
    }
    if (this.tempQueueOrKey != null) {
      this.routingKey = this.tempQueueOrKey;
      this.tempQueueOrKey = null;
    }
    return new SpringAMQPProducer(this);
  }

  @Override public Consumer createConsumer(Processor processor) throws Exception {
    if (this.exchangeName == null) {
      throw new IllegalStateException("Cannot have null exchange name");
    }
    if (this.tempQueueOrKey != null) {
      this.queueName = this.tempQueueOrKey;
      this.tempQueueOrKey = null;
      if (this.exchangeType == null) {
        this.exchangeType = "fanout";
      }
    }
    if (this.queueName == null) {
      throw new IllegalStateException("Cannot have null queue name for " + getEndpointUri());
    }
    return new SpringAMQPConsumer(this, processor);
  }

  public AmqpAdmin getAmqpAdministration() {
    return amqpAdministration;
  }

  public void setAmqpAdministration(AmqpAdmin amqpAdministration) {
    this.amqpAdministration = amqpAdministration;
  }

  public AmqpTemplate getAmqpTemplate() {
    return amqpTemplate;
  }

  public void setAmqpTemplate(AmqpTemplate amqpTemplate) {
    this.amqpTemplate = amqpTemplate;
  }

  public int getPrefetchCount() {
    return prefetchCount;
  }

  public void setPrefetchCount(int prefetchCount) {
    this.prefetchCount = prefetchCount;
  }

  public int getConcurrentConsumers() {
    return concurrentConsumers;
  }

  public void setConcurrentConsumers(int concurrentConsumers) {
    this.concurrentConsumers = concurrentConsumers;
  }

  public boolean isTransactional() {
    return transactional;
  }

  public void setTransactional(boolean transactional) {
    this.transactional = transactional;
  }

  public String getExchangeName() {
    return exchangeName;
  }

  public void setExchangeName(String exchangeName) {
    this.exchangeName = exchangeName;
  }

  public String getQueueName() {
    return queueName;
  }

  public boolean isUsingDefaultExchange() {
    return DEFAULT_EXCHANGE_NAME.equals(this.exchangeName);
  }

  public void setQueueName(String queueName) {
    this.queueName = queueName;
  }

  public String getRoutingKey() {
    return routingKey;
  }

  public void setRoutingKey(String routingKey) {
    this.routingKey = routingKey;
  }

  public boolean isAutodelete() {
    return autodelete;
  }

  public void setAutodelete(boolean autodelete) {
    this.autodelete = autodelete;
  }

  public boolean isDurable() {
    return durable;
  }

  public void setDurable(boolean durable) {
    this.durable = durable;
  }

  public String getType() {
    return exchangeType;
  }

  public void setType(String exchangeType) {
    this.exchangeType = exchangeType;
  }

  public boolean isExclusive() {
    return exclusive;
  }

  public void setExclusive(boolean exclusive) {
    this.exclusive = exclusive;
  }

  public Integer getTimeToLive() {
    return timeToLive;
  }

  public void setTimeToLive(Integer timeToLive) {
    this.timeToLive = timeToLive;
  }

  public long getIdleThreadKeepAliveMillis() {
    return idleThreadKeepAliveMillis;
  }

  public void setIdleThreadKeepAliveMillis(long idleThreadKeepAliveMillis) {
    this.idleThreadKeepAliveMillis = idleThreadKeepAliveMillis;
  }

  public int getThreadPoolIdleSize() {
    return threadPoolIdleSize;
  }

  public void setThreadPoolIdleSize(int threadPoolIdleSize) {
    if (threadPoolIdleSize == 0) {
      throw new IllegalArgumentException("Cannot set thread pool size to 0!");
    }
    this.threadPoolIdleSize = threadPoolIdleSize;
  }

  public int getThreadPoolMaxSize() {
    return threadPoolMaxSize;
  }

  public void setThreadPoolMaxSize(int threadPoolMaxSize) {
    if (threadPoolIdleSize == 0) {
      throw new IllegalArgumentException("Cannot set thread pool size to 0!");
    }
    this.threadPoolMaxSize = threadPoolMaxSize;
  }

  @Override public boolean isSingleton() {
    return false;
  }

  @Override protected String createEndpointUri() {
    StringBuilder builder = new StringBuilder("spring-amqp:").append(this.exchangeName);
    if (this.queueName != null) {
      builder.append(":").append(this.queueName);
    }
    if (this.routingKey != null) {
      builder.append(":").append(this.routingKey);
    }
    builder.append("?").append("type=").append(this.exchangeType);
    builder.append("&autodelete=").append(this.autodelete);
    builder.append("&concurrentConsumers=").append(this.concurrentConsumers);
    builder.append("&durable=").append(this.durable);
    builder.append("&exclusive=").append(this.exclusive);
    builder.append("&transactional=").append(this.transactional);
    return builder.toString();
  }

  org.springframework.amqp.core.Exchange createAMQPExchange() {
    if (this.exchangeType == null || "direct".equals(this.exchangeType)) {
      return new DirectExchange(this.exchangeName, this.durable, this.autodelete);
    } else {
      if ("fanout".equals(this.exchangeType)) {
        return new FanoutExchange(this.exchangeName, this.durable, this.autodelete);
      } else {
        if ("headers".equals(this.exchangeType)) {
          return new HeadersExchange(this.exchangeName, this.durable, this.autodelete);
        } else {
          if ("topic".equals(this.exchangeType)) {
            return new TopicExchange(this.exchangeName, this.durable, this.autodelete);
          } else {
            return new DirectExchange(this.exchangeName, this.durable, this.autodelete);
          }
        }
      }
    }
  }
}