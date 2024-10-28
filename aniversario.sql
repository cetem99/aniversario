SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema lembrar_aniversarios
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `lembrar_aniversarios` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `lembrar_aniversarios` ;

-- -----------------------------------------------------
-- Table `lembrar_aniversarios`.`usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lembrar_aniversarios`.`usuario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(191) NOT NULL,
  `nome` VARCHAR(255) NOT NULL,
  `data_nascimento` DATE NOT NULL,
  `senha` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email` (`email` ASC) VISIBLE)
ENGINE = MyISAM
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `lembrar_aniversarios`.`aniversariantes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `lembrar_aniversarios`.`aniversariantes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(255) NOT NULL,
  `data_aniversario` DATE NOT NULL DEFAULT '2000-01-01',
  `email` VARCHAR(255) NOT NULL,
  `telefone` VARCHAR(20) NOT NULL,
  `notificacao` VARCHAR(50) NOT NULL,
  `felicitacao` TEXT NULL DEFAULT NULL,
  `usuario_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_aniversariantes_usuario_idx` (`usuario_id` ASC),
  CONSTRAINT `fk_aniversariantes_usuario`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `usuario` (`id`)
    ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


select * from usuario;
