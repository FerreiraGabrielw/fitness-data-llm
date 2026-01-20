-- ==========================================
-- SCRIPT DE CRIAÇÃO DO BANCO DE DADOS
-- ==========================================

-- 1. Definição de Estrutura Inicial
CREATE SCHEMA IF NOT EXISTS fitness;
SET search_path TO fitness;

-- 2. Criação das Tabelas (Ordem respeitando chaves estrangeiras)

-- Tabela: exercises
CREATE TABLE exercises (
    exercise_id SERIAL PRIMARY KEY,
    exercise_name TEXT NOT NULL UNIQUE,
    exercise_type TEXT,
    is_cardio BOOLEAN,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela: workouts
CREATE TABLE workouts (
    workout_id SERIAL PRIMARY KEY,
    workout_name TEXT,
    workout_date DATE NOT NULL,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    duration_minutes NUMERIC(5,2),
    description TEXT,
    source TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabela: workout_exercises
CREATE TABLE workout_exercises (
    workout_exercise_id SERIAL PRIMARY KEY,
    workout_id INT NOT NULL REFERENCES workouts(workout_id) ON DELETE CASCADE,
    exercise_id INT NOT NULL REFERENCES exercises(exercise_id),
    exercise_order INT,
    superset_id INT,
    notes TEXT
);

-- Tabela: sets
CREATE TABLE sets (
    set_id SERIAL PRIMARY KEY,
    workout_exercise_id INT NOT NULL REFERENCES workout_exercises(workout_exercise_id) ON DELETE CASCADE,
    set_index INT NOT NULL,
    set_type TEXT,
    weight_kg NUMERIC(6,2),
    reps INT,
    distance_km NUMERIC(6,3),
    duration_seconds INT,
    rpe NUMERIC(3,1),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. Criação de Índices para Performance
CREATE INDEX idx_workouts_date ON workouts(workout_date);
CREATE INDEX idx_exercises_name ON exercises(exercise_name);
CREATE INDEX idx_sets_type ON sets(set_type);
CREATE INDEX idx_sets_workout_exercise ON sets(workout_exercise_id);