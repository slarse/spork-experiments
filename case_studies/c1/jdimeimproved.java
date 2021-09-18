package org.apache.ibatis.annotations;
import org.apache.ibatis.builder.annotation.StatementAnnotationMetadata;
import org.apache.ibatis.mapping.SqlCommandType;
import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Repeatable;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Documented @Retention(value = RetentionPolicy.RUNTIME) @Target(value = { ElementType.METHOD }) @Repeatable(value = Select.List.class) @StatementAnnotationMetadata(commandType = SqlCommandType.SELECT) public @interface Select {
  String[] value();

  String databaseId() default "";

  @Documented @Retention(value = RetentionPolicy.RUNTIME) @Target(value = { ElementType.METHOD }) @StatementAnnotationMetadata(commandType = SqlCommandType.SELECT) @interface List {
    Select[] value();
  }
}