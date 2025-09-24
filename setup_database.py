import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv(".env")

def create_database():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST") or "localhost",
            user=os.getenv("MYSQL_USER") or "root",
            password=os.getenv("MYSQL_PASSWORD") or "admin4B",
        )

        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute(
                f"DROP DATABASE IF EXISTS {os.getenv('MYSQL_DB')}"
            )

            cursor.execute(
                f"CREATE SCHEMA IF NOT EXISTS {os.getenv('MYSQL_DB')} DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci"
            )
            print(f"Base de datos '{os.getenv('MYSQL_DB')}' creada o ya existente.")

            cursor.execute(f"USE {os.getenv('MYSQL_DB')}")

            create_usuarios_table = """
            CREATE TABLE IF NOT EXISTS usuarios (
                `id` INT NOT NULL AUTO_INCREMENT,
                `nombre` VARCHAR(45) NOT NULL,
                `apellido` VARCHAR(45) NOT NULL,
                `email` VARCHAR(255) NOT NULL,
                `password` VARCHAR(255) NOT NULL,
                `creado_en` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                `actualizado_en` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                UNIQUE INDEX `email` (`email` ASC) VISIBLE)
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8mb4
            COLLATE = utf8mb4_0900_ai_ci;
            """

            cursor.execute(create_usuarios_table)
            print("Tabla 'usuarios' creada exitosamente.")

            create_citas_table = f"""
            CREATE TABLE IF NOT EXISTS citas (
                `id` INT NOT NULL AUTO_INCREMENT,
                `cita` TEXT NOT NULL,
                `autor_id` INT NOT NULL,
                `creado_en` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                `actualizado_en` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                PRIMARY KEY (`id`),
                INDEX `fk_citas_usuarios_idx` (`autor_id` ASC) VISIBLE,
                CONSTRAINT `fk_citas_usuarios`
                    FOREIGN KEY (`autor_id`)
                    REFERENCES `{os.getenv('MYSQL_DB')}`.`usuarios` (`id`)
                    ON DELETE CASCADE)
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8mb4
            COLLATE = utf8mb4_0900_ai_ci;
            """

            cursor.execute(create_citas_table)
            print("Tabla 'citas' creada exitosamente.")

            create_favoritos_table = f"""
            CREATE TABLE IF NOT EXISTS favoritos (
                `id` INT NOT NULL AUTO_INCREMENT,
                `usuario_id` INT NOT NULL,
                `cita_id` INT NOT NULL,
                PRIMARY KEY (`id`),
                INDEX `fk_favoritos_usuarios_idx` (`usuario_id` ASC) VISIBLE,
                INDEX `fk_favoritos_citas_idx` (`cita_id` ASC) VISIBLE,
                CONSTRAINT `fk_favoritos_citas`
                    FOREIGN KEY (`cita_id`)
                    REFERENCES `{os.getenv('MYSQL_DB')}`.`citas` (`id`)
                    ON DELETE CASCADE,
            CONSTRAINT `fk_favoritos_usuarios`
                FOREIGN KEY (`usuario_id`)
                REFERENCES `{os.getenv('MYSQL_DB')}`.`usuarios` (`id`)
                ON DELETE CASCADE)
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8mb4
            COLLATE = utf8mb4_0900_ai_ci;
            """

            cursor.execute(create_favoritos_table)
            print("Tabla 'favoritos' creada exitosamente.")

            cursor.execute("SET SQL_MODE=@OLD_SQL_MODE;")
            cursor.execute("SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;")
            cursor.execute("SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;")

            connection.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexión a MySQL cerrada.")


if __name__ == "__main__":
    create_database()
