CREATE TABLE discentes (
    id_discente INT PRIMARY KEY,
    matricula VARCHAR(50) NOT NULL
);

CREATE TABLE cursos (
    id_curso_sigaa INT PRIMARY KEY,
    nome_curso VARCHAR(255)
);

CREATE TABLE tipos_bolsa (
    id_tipo_bolsa INT PRIMARY KEY,
    descricao_bolsa VARCHAR(255)
);

CREATE TABLE unidades_pagadoras (
    id_unidade_pagadora INT PRIMARY KEY,
    nome_unidade VARCHAR(255)
);

CREATE TABLE bolsas (
    id INT PRIMARY KEY,
    id_discente INT,
    id_curso_sigaa INT,
    id_tipo_bolsa INT,
    inicio DATE,
    fim DATE,
    id_unidade_pagadora INT,
    FOREIGN KEY (id_discente) REFERENCES discentes(id_discente),
    FOREIGN KEY (id_curso_sigaa) REFERENCES cursos(id_curso_sigaa),
    FOREIGN KEY (id_tipo_bolsa) REFERENCES tipos_bolsa(id_tipo_bolsa),
    FOREIGN KEY (id_unidade_pagadora) REFERENCES unidades_pagadoras(id_unidade_pagadora)
);