-- Schema

CREATE TABLE restaurants (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    is_open BOOLEAN DEFAULT TRUE
);

CREATE TABLE customers (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR,
    total_orders INT DEFAULT 0,
    refunds_last_30_days INT DEFAULT 0
);

CREATE TABLE orders (
    id VARCHAR PRIMARY KEY,
    customer_id VARCHAR REFERENCES customers(id),
    restaurant_id VARCHAR REFERENCES restaurants(id),
    status VARCHAR NOT NULL, -- pending, confirmed, preparing, on_the_way, delivered, cancelled
    total_value NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    estimated_delivery_at TIMESTAMP,
    delivered_at TIMESTAMP
);

-- Seed: Restaurantes
INSERT INTO restaurants VALUES
    ('rest-001', 'Burger King Aldeota', TRUE),
    ('rest-002', 'Pizza Hut Meireles', FALSE),
    ('rest-003', 'Sushi Express', TRUE);

-- Seed: Clientes
INSERT INTO customers VALUES
    ('cust-001', 'João Silva',    'joao@email.com',   45, 1),
    ('cust-002', 'Maria Oliveira','maria@email.com',   3, 0),
    ('cust-003', 'Carlos Souza',  'carlos@email.com', 120, 4);

-- Seed: Pedidos — vários cenários para testar os workflows

-- Pedido entregue, valor baixo (resolução automática ok)
INSERT INTO orders VALUES (
    'order-001', 'cust-001', 'rest-001', 'delivered', 32.90,
    NOW() - INTERVAL '2 hours',
    NOW() - INTERVAL '1 hour 30 minutes',
    NOW() - INTERVAL '1 hour 15 minutes'
);

-- Pedido atrasado, ainda não entregue
INSERT INTO orders VALUES (
    'order-002', 'cust-002', 'rest-002', 'on_the_way', 45.00,
    NOW() - INTERVAL '3 hours',
    NOW() - INTERVAL '1 hour',
    NULL
);

-- Pedido com valor alto — vai acionar guardrail de reembolso > R$50
INSERT INTO orders VALUES (
    'order-003', 'cust-003', 'rest-003', 'delivered', 89.90,
    NOW() - INTERVAL '1 hour',
    NOW() - INTERVAL '30 minutes',
    NOW() - INTERVAL '20 minutes'
);

-- Pedido cancelado
INSERT INTO orders VALUES (
    'order-004', 'cust-001', 'rest-002', 'cancelled', 27.50,
    NOW() - INTERVAL '4 hours',
    NOW() - INTERVAL '3 hours',
    NULL
);

-- Pedido entregue com atraso
INSERT INTO orders VALUES (
    'order-005', 'cust-002', 'rest-001', 'delivered', 38.00,
    NOW() - INTERVAL '5 hours',
    NOW() - INTERVAL '3 hours 30 minutes',
    NOW() - INTERVAL '2 hours 45 minutes'
);