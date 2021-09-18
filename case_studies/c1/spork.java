/**
<<<<<<< LEFT
 *    Copyright 2009-2019 the original author or authors.
=======
 *    Copyright 2009-2020 the original author or authors.
>>>>>>> RIGHT
 *
 *    Licensed under the Apache License, Version 2.0 (the "License");
 *    you may not use this file except in compliance with the License.
 *    You may obtain a copy of the License at
 *
 *       http://www.apache.org/licenses/LICENSE-2.0
 *
 *    Unless required by applicable law or agreed to in writing, software
 *    distributed under the License is distributed on an "AS IS" BASIS,
 *    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *    See the License for the specific language governing permissions and
 *    limitations under the License.
 */
package org.apache.ibatis.annotations;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Repeatable;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;
import org.apache.ibatis.builder.annotation.StatementAnnotationMetadata;
import org.apache.ibatis.mapping.SqlCommandType;


/**
 * The annotation that specify an SQL for retrieving record(s).
 *
 * <p>
 * <b>How to use:</b>
 *
 * <pre>
 * public interface UserMapper {
 * &#064;Select("SELECT id, name FROM users WHERE id = #{id}")
 * User selectById(int id);
 * }
 * </pre>
 *
 * @author Clinton Begin
 */
@Documented
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
@Repeatable(Select.List.class)
@StatementAnnotationMetadata(commandType = SqlCommandType.SELECT)
public @interface Select {
  /**
   * Returns an SQL for retrieving record(s).
   *
   * @return an SQL for retrieving record(s)
   */
  String[] value();

  /**
   * @return A database id that correspond this statement
   * @since 3.5.1
   */
  String databaseId() default "";

  /**
   * The container annotation for {@link Select}.
   *
   * @author Kazuki Shimizu
   * @since 3.5.1
   */
  @Documented
  @Retention(RetentionPolicy.RUNTIME)
  @Target(ElementType.METHOD)
  @StatementAnnotationMetadata(commandType = SqlCommandType.SELECT)
  @interface List {
    Select[] value();
  }
}