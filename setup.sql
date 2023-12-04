USE empotrados;

CREATE TABLE recipientes(
	recipiente_id INT PRIMARY KEY AUTO_INCREMENT,
    nombre_recipiente VARCHAR(50) NOT NULL,
    longitud INT NOT NULL
);

CREATE TABLE cantidades(
	cantidad_id INT PRIMARY KEY AUTO_INCREMENT,
    cantidad INT NOT NULL,
    fecha DATETIME NOT NULL,
    recipiente_id INT,
    
    FOREIGN KEY (recipiente_id) REFERENCES recipientes(recipiente_id)
);