# 🎯 하네스 엔지니어링 - 실전 예제 모음

**작성일:** 2026년 3월  
**주제:** 프로덕션급 테스트 하네스 구현 가이드

---

## 📋 목차

1. [완전한 테스트 하네스 구현](#1-완전한-테스트-하네스-구현)
2. [마이크로서비스 테스트](#2-마이크로서비스-테스트)
3. [Harness CI/CD 파이프라인](#3-harness-cicd-파이프라인)
4. [성능 및 부하 테스트 하네스](#4-성능-및-부하-테스트-하네스)
5. [AI 기반 테스트 생성](#5-ai-기반-테스트-생성)

---

## 1. 완전한 테스트 하네스 구현

### 1.1 전자상거래 애플리케이션 테스트 하네스

```python
# project_root/
# ├── src/
# │   ├── models/
# │   │   ├── user.py
# │   │   └── product.py
# │   ├── services/
# │   │   ├── user_service.py
# │   │   └── payment_service.py
# │   └── api/
# │       └── orders.py
# ├── tests/
# │   ├── conftest.py  # 공유 픽스처
# │   ├── unit/
# │   ├── integration/
# │   ├── e2e/
# │   └── fixtures/
# └── pytest.ini

# src/models/user.py
from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    SELLER = "seller"

class User(BaseModel):
    id: str
    email: EmailStr
    password_hash: str
    name: str
    role: UserRole = UserRole.CUSTOMER
    created_at: datetime = datetime.now()
    is_active: bool = True
    
    @validator('name')
    def name_not_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Name cannot be empty')
        return v.strip()

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

# src/models/product.py
class Product(BaseModel):
    id: str
    name: str
    price: float
    quantity_available: int
    description: str = ""
    
    def is_available(self, quantity: int = 1) -> bool:
        return self.quantity_available >= quantity
    
    def reduce_quantity(self, quantity: int):
        if quantity > self.quantity_available:
            raise ValueError("Not enough quantity")
        self.quantity_available -= quantity

# src/services/user_service.py
from typing import Optional
import hashlib

class UserService:
    def __init__(self, repository):
        self.repo = repository
    
    def create_user(self, user_data: UserCreate) -> User:
        # 중복 확인
        if self.repo.get_by_email(user_data.email):
            raise ValueError(f"User with email {user_data.email} already exists")
        
        # 비밀번호 해싱
        password_hash = hashlib.sha256(user_data.password.encode()).hexdigest()
        
        user = User(
            id=self._generate_id(),
            email=user_data.email,
            password_hash=password_hash,
            name=user_data.name
        )
        
        return self.repo.save(user)
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.repo.get(user_id)
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.repo.get_by_email(email)
        if not user:
            return None
        
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash != password_hash:
            return None
        
        return user if user.is_active else None
    
    @staticmethod
    def _generate_id():
        import uuid
        return str(uuid.uuid4())

# src/services/payment_service.py
from enum import Enum
from dataclasses import dataclass
from typing import Optional

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

@dataclass
class Payment:
    id: str
    order_id: str
    amount: float
    status: PaymentStatus
    method: str
    transaction_id: Optional[str] = None

class PaymentGateway:
    """결제 게이트웨이 인터페이스"""
    def charge(self, amount: float, method: str) -> dict:
        raise NotImplementedError

class PaymentService:
    def __init__(self, gateway: PaymentGateway, repository):
        self.gateway = gateway
        self.repo = repository
    
    def process_payment(self, order_id: str, amount: float, method: str) -> Payment:
        """결제 처리"""
        try:
            result = self.gateway.charge(amount, method)
            
            payment = Payment(
                id=self._generate_id(),
                order_id=order_id,
                amount=amount,
                status=PaymentStatus.COMPLETED,
                method=method,
                transaction_id=result.get("transaction_id")
            )
            
            return self.repo.save(payment)
        
        except Exception as e:
            payment = Payment(
                id=self._generate_id(),
                order_id=order_id,
                amount=amount,
                status=PaymentStatus.FAILED,
                method=method
            )
            self.repo.save(payment)
            raise
    
    @staticmethod
    def _generate_id():
        import uuid
        return str(uuid.uuid4())

# tests/conftest.py
import pytest
from unittest.mock import Mock, MagicMock
import tempfile
import sqlite3

from src.models.user import User, UserRole
from src.models.product import Product
from src.services.user_service import UserService
from src.services.payment_service import PaymentService, PaymentGateway

# ============== Fixtures ==============

@pytest.fixture(scope="session")
def test_db():
    """테스트용 데이터베이스"""
    db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    connection = sqlite3.connect(db_file.name)
    
    # 테이블 생성
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE,
            password_hash TEXT,
            name TEXT,
            role TEXT,
            created_at TIMESTAMP,
            is_active BOOLEAN
        )
    """)
    cursor.execute("""
        CREATE TABLE products (
            id TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            quantity_available INTEGER,
            description TEXT
        )
    """)
    connection.commit()
    
    yield connection
    
    connection.close()

@pytest.fixture
def mock_user_repo():
    """사용자 저장소 Mock"""
    repo = Mock()
    repo.users = {}
    
    def save(user):
        repo.users[user.id] = user
        return user
    
    def get(user_id):
        return repo.users.get(user_id)
    
    def get_by_email(email):
        for user in repo.users.values():
            if user.email == email:
                return user
        return None
    
    repo.save = save
    repo.get = get
    repo.get_by_email = get_by_email
    
    return repo

@pytest.fixture
def mock_payment_repo():
    """결제 저장소 Mock"""
    repo = Mock()
    repo.payments = {}
    
    def save(payment):
        repo.payments[payment.id] = payment
        return payment
    
    def get(payment_id):
        return repo.payments.get(payment_id)
    
    repo.save = save
    repo.get = get
    
    return repo

@pytest.fixture
def mock_payment_gateway():
    """결제 게이트웨이 Mock"""
    gateway = Mock(spec=PaymentGateway)
    gateway.charge.return_value = {
        "transaction_id": "txn_123456",
        "status": "success"
    }
    return gateway

@pytest.fixture
def user_service(mock_user_repo):
    """사용자 서비스"""
    return UserService(mock_user_repo)

@pytest.fixture
def payment_service(mock_payment_gateway, mock_payment_repo):
    """결제 서비스"""
    return PaymentService(mock_payment_gateway, mock_payment_repo)

@pytest.fixture
def sample_user():
    """샘플 사용자"""
    return User(
        id="user_1",
        email="alice@example.com",
        password_hash="hashed_password",
        name="Alice Johnson",
        role=UserRole.CUSTOMER
    )

@pytest.fixture
def sample_product():
    """샘플 상품"""
    return Product(
        id="product_1",
        name="Laptop",
        price=999.99,
        quantity_available=10,
        description="High-performance laptop"
    )

# tests/unit/test_user_service.py
import pytest
from src.models.user import UserCreate

class TestUserServiceCreation:
    """사용자 생성 테스트"""
    
    def test_create_user_success(self, user_service, mock_user_repo):
        """성공적인 사용자 생성"""
        user_data = UserCreate(
            email="bob@example.com",
            password="secure_password",
            name="Bob Smith"
        )
        
        user = user_service.create_user(user_data)
        
        assert user.email == "bob@example.com"
        assert user.name == "Bob Smith"
        assert user.is_active == True
        assert mock_user_repo.get(user.id) == user
    
    def test_create_user_duplicate_email(self, user_service, mock_user_repo, sample_user):
        """중복 이메일로 사용자 생성 실패"""
        # 기존 사용자 저장
        mock_user_repo.save(sample_user)
        
        user_data = UserCreate(
            email="alice@example.com",  # 같은 이메일
            password="password",
            name="Alice 2"
        )
        
        with pytest.raises(ValueError, match="already exists"):
            user_service.create_user(user_data)
    
    def test_create_user_empty_name(self, user_service):
        """빈 이름으로 사용자 생성 실패"""
        user_data = UserCreate(
            email="charlie@example.com",
            password="password",
            name=""  # 빈 이름
        )
        
        with pytest.raises(ValueError):
            user_service.create_user(user_data)
    
    def test_create_user_invalid_email(self, user_service):
        """유효하지 않은 이메일로 사용자 생성 실패"""
        user_data = UserCreate(
            email="invalid-email",  # 유효하지 않은 이메일
            password="password",
            name="David"
        )
        
        with pytest.raises(ValueError):
            user_service.create_user(user_data)

class TestUserServiceAuthentication:
    """사용자 인증 테스트"""
    
    def test_authenticate_success(self, user_service, mock_user_repo, sample_user):
        """성공적인 인증"""
        mock_user_repo.save(sample_user)
        
        # 실제 비밀번호를 사용하여 해시 생성
        password = "test_password"
        import hashlib
        sample_user.password_hash = hashlib.sha256(password.encode()).hexdigest()
        mock_user_repo.save(sample_user)
        
        user = user_service.authenticate("alice@example.com", password)
        
        assert user is not None
        assert user.id == "user_1"
    
    def test_authenticate_invalid_password(self, user_service, mock_user_repo, sample_user):
        """잘못된 비밀번호로 인증 실패"""
        mock_user_repo.save(sample_user)
        
        user = user_service.authenticate("alice@example.com", "wrong_password")
        
        assert user is None
    
    def test_authenticate_nonexistent_user(self, user_service):
        """존재하지 않는 사용자 인증"""
        user = user_service.authenticate("nonexistent@example.com", "password")
        
        assert user is None
    
    def test_authenticate_inactive_user(self, user_service, mock_user_repo, sample_user):
        """비활성 사용자 인증 실패"""
        sample_user.is_active = False
        mock_user_repo.save(sample_user)
        
        import hashlib
        password = "test_password"
        sample_user.password_hash = hashlib.sha256(password.encode()).hexdigest()
        mock_user_repo.save(sample_user)
        
        user = user_service.authenticate("alice@example.com", password)
        
        assert user is None

# tests/unit/test_payment_service.py
import pytest
from src.services.payment_service import PaymentStatus

class TestPaymentService:
    """결제 서비스 테스트"""
    
    def test_process_payment_success(self, payment_service, mock_payment_gateway):
        """성공적인 결제"""
        payment = payment_service.process_payment(
            order_id="order_1",
            amount=100.00,
            method="credit_card"
        )
        
        assert payment.status == PaymentStatus.COMPLETED
        assert payment.amount == 100.00
        assert payment.method == "credit_card"
        assert payment.transaction_id == "txn_123456"
        
        # 게이트웨이 호출 확인
        mock_payment_gateway.charge.assert_called_once_with(100.00, "credit_card")
    
    def test_process_payment_gateway_failure(self, payment_service, mock_payment_gateway):
        """결제 게이트웨이 실패"""
        mock_payment_gateway.charge.side_effect = Exception("Gateway error")
        
        with pytest.raises(Exception):
            payment_service.process_payment(
                order_id="order_1",
                amount=100.00,
                method="credit_card"
            )
    
    def test_process_payment_records_failure(self, payment_service, mock_payment_gateway, mock_payment_repo):
        """실패한 결제 기록"""
        mock_payment_gateway.charge.side_effect = Exception("Gateway error")
        
        with pytest.raises(Exception):
            payment_service.process_payment(
                order_id="order_1",
                amount=100.00,
                method="credit_card"
            )
        
        # 실패한 결제 기록 확인
        assert len(mock_payment_repo.payments) == 1
        payment = list(mock_payment_repo.payments.values())[0]
        assert payment.status == PaymentStatus.FAILED

# tests/unit/test_product_model.py
class TestProductModel:
    """상품 모델 테스트"""
    
    def test_product_availability(self, sample_product):
        """상품 가용성 확인"""
        assert sample_product.is_available(5) == True
        assert sample_product.is_available(10) == True
        assert sample_product.is_available(11) == False
    
    def test_product_reduce_quantity_success(self, sample_product):
        """상품 수량 감소"""
        sample_product.reduce_quantity(3)
        assert sample_product.quantity_available == 7
    
    def test_product_reduce_quantity_insufficient(self, sample_product):
        """수량 부족으로 감소 실패"""
        with pytest.raises(ValueError, match="Not enough quantity"):
            sample_product.reduce_quantity(20)

# tests/integration/test_checkout_workflow.py
class TestCheckoutWorkflow:
    """체크아웃 워크플로우 통합 테스트"""
    
    def test_complete_checkout_flow(
        self,
        user_service,
        payment_service,
        mock_user_repo,
        sample_user,
        sample_product
    ):
        """전체 체크아웃 프로세스"""
        # 1. 사용자 저장
        mock_user_repo.save(sample_user)
        
        # 2. 사용자 조회
        user = user_service.get_user(sample_user.id)
        assert user is not None
        
        # 3. 상품 가용성 확인
        assert sample_product.is_available(2)
        
        # 4. 결제 처리
        payment = payment_service.process_payment(
            order_id="order_123",
            amount=1999.98,  # 999.99 * 2
            method="credit_card"
        )
        
        assert payment.status == PaymentStatus.COMPLETED
        
        # 5. 상품 수량 업데이트
        sample_product.reduce_quantity(2)
        assert sample_product.quantity_available == 8

# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    e2e: marks tests as end-to-end tests
```

### 1.2 테스트 실행

```bash
# 모든 테스트 실행
pytest

# 단위 테스트만 실행
pytest tests/unit -v

# 특정 테스트 클래스 실행
pytest tests/unit/test_user_service.py::TestUserServiceCreation -v

# 테스트 커버리지 확인
pytest --cov=src --cov-report=html

# 병렬 실행 (pytest-xdist)
pytest -n auto

# 느린 테스트 제외
pytest -m "not slow"
```

---

## 2. 마이크로서비스 테스트

### 2.1 Contract Testing (Pact)

```python
# tests/contract/test_user_service_contract.py
from pact import Consumer, Provider
import json

# Consumer 테스트: OrderService가 UserService를 의존
def test_order_service_gets_user():
    """OrderService가 UserService에서 사용자 조회"""
    
    pact = Consumer("OrderService").has_state(
        "user with id 123 exists"
    ).upon_receiving(
        "a request for user details"
    ).with_request(
        "get", "/api/users/123"
    ).will_respond_with(
        200,
        body={
            "id": "123",
            "name": "Alice",
            "email": "alice@example.com",
            "premium": True
        }
    )
    
    with pact.start_service() as interaction:
        # OrderService가 사용자를 조회
        import requests
        response = requests.get("http://localhost:8000/api/users/123")
        
        assert response.status_code == 200
        user = response.json()
        assert user["name"] == "Alice"
        assert user["premium"] == True
    
    pact.verify()
    pact.write_file(version="2.0.0")  # pact 파일 저장

# Provider 테스트: UserService가 계약 준수
import subprocess

def test_user_service_honors_contract():
    """UserService가 OrderService와의 계약 준수"""
    
    pact = Provider("UserService").given(
        "user with id 123 exists"
    ).upon_receiving(
        "a request for user details"
    ).with_request(
        "get", "/api/users/123"
    ).will_respond_with(
        200,
        body={
            "id": "123",
            "name": "Alice",
            "email": "alice@example.com",
            "premium": True
        }
    )
    
    # UserService 시작
    # ... start user service
    
    # Pact 검증
    result = pact.verify_with_provider()
    
    assert result == True
```

### 2.2 API 게이트웨이 테스트

```python
# tests/integration/test_api_gateway.py
import pytest
import httpx
from unittest.mock import patch, AsyncMock

@pytest.fixture
async def api_client():
    """API 클라이언트"""
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        yield client

@pytest.mark.asyncio
class TestAPIGateway:
    """API 게이트웨이 통합 테스트"""
    
    async def test_request_routing(self, api_client):
        """요청 라우팅"""
        response = await api_client.get("/api/users/123")
        assert response.status_code == 200
    
    async def test_rate_limiting(self, api_client):
        """Rate Limiting"""
        for i in range(101):
            response = await api_client.get("/api/health")
        
        # 100 요청 후 제한
        assert response.status_code == 429
    
    async def test_circuit_breaker(self, api_client):
        """Circuit Breaker 패턴"""
        # 서비스 실패 5회
        for i in range(5):
            response = await api_client.get("/api/unreliable-service")
            assert response.status_code == 500
        
        # Circuit이 열림 (빠른 실패)
        response = await api_client.get("/api/unreliable-service")
        assert response.status_code == 503  # Service Unavailable
    
    async def test_request_tracing(self, api_client):
        """분산 추적 (Distributed Tracing)"""
        response = await api_client.get(
            "/api/orders/123",
            headers={"X-Trace-ID": "trace_xyz"}
        )
        
        # 응답에 trace ID 포함
        assert response.headers.get("X-Trace-ID") == "trace_xyz"
    
    @patch('services.payment_service.charge')
    async def test_fallback_behavior(self, mock_charge, api_client):
        """폴백 동작"""
        mock_charge.side_effect = Exception("Service down")
        
        # 주문 생성 요청 (결제 서비스 실패)
        response = await api_client.post(
            "/api/orders",
            json={"user_id": "123", "items": []}
        )
        
        # 폴백: 주문은 생성되지만 pending 상태
        assert response.status_code == 200
        order = response.json()
        assert order["status"] == "pending"
```

---

## 3. Harness CI/CD 파이프라인

### 3.1 Harness 파이프라인 YAML

```yaml
# .harness/build-and-deploy.yaml
pipeline:
  name: Build and Deploy Pipeline
  identifier: build_deploy_pipeline
  projectIdentifier: myproject
  orgIdentifier: myorg
  
  stages:
    # Stage 1: 빌드 및 테스트
    - stage:
        name: Build and Test
        identifier: build_test_stage
        type: CI
        spec:
          cloneCodebase: true
          caching:
            enabled: true
          steps:
            # 1. 의존성 설치
            - step:
                type: Run
                identifier: installDeps
                name: Install Dependencies
                spec:
                  shell: Bash
                  command: |
                    pip install -r requirements.txt
                    pip install pytest pytest-cov
            
            # 2. 린트 검사
            - step:
                type: Run
                identifier: lint
                name: Lint Code
                spec:
                  shell: Bash
                  command: |
                    pip install flake8 black
                    black --check src/
                    flake8 src/ --max-line-length=100
            
            # 3. 단위 테스트 (Test Intelligence 활용)
            - step:
                type: Run
                identifier: unitTests
                name: Run Unit Tests
                spec:
                  shell: Bash
                  command: |
                    pytest tests/unit \
                      --junit-xml=test-results/unit-tests.xml \
                      --cov=src \
                      --cov-report=xml \
                      --test-intelligence-enabled
                  reports:
                    type: JUnit
                    paths:
                      - test-results/unit-tests.xml
                    uploadGac: true
            
            # 4. 빌드 이미지
            - step:
                type: BuildAndPushDockerRegistry
                identifier: buildImage
                name: Build and Push Docker Image
                spec:
                  connectorRef: dockerhub_connector
                  repo: myorg/myapp
                  tags:
                    - <+pipeline.execution.number>
                    - latest
                  dockerfile: Dockerfile
                  context: .
    
    # Stage 2: 통합 테스트 (선택적)
    - stage:
        name: Integration Tests
        identifier: integration_tests_stage
        type: CI
        when:
          stageStatus: Success
          condition: <+trigger.event> == "push" && <+pipeline.triggeredBy.branch> == "main"
        spec:
          cloneCodebase: true
          steps:
            - step:
                type: Run
                identifier: integrationTests
                name: Run Integration Tests
                spec:
                  shell: Bash
                  command: |
                    docker-compose -f docker-compose.test.yml up -d
                    sleep 10
                    pytest tests/integration -v
                    docker-compose -f docker-compose.test.yml down
                  reports:
                    type: JUnit
                    paths:
                      - test-results/integration-tests.xml
    
    # Stage 3: 배포 (Dev)
    - stage:
        name: Deploy to Dev
        identifier: deploy_dev_stage
        type: Deployment
        when:
          stageStatus: Success
        spec:
          deploymentType: Kubernetes
          service:
            serviceRef: myapp_service
            serviceInputs:
              - name: namespace
                value: dev
          environment:
            environmentRef: dev_environment
          infrastructure:
            infrastructureDefinition:
              type: KubernetesDirect
              spec:
                connectorRef: k8s_dev_cluster
          execution:
            steps:
              - step:
                  type: ShellScript
                  identifier: preDeploy
                  name: Pre-deployment Checks
                  spec:
                    shell: Bash
                    script: |
                      echo "Running pre-deployment checks..."
                      kubectl cluster-info
              
              - step:
                  type: Apply
                  identifier: deployApp
                  name: Deploy Application
                  spec:
                    skipDryRun: false
              
              - step:
                  type: Verify
                  identifier: smokeTest
                  name: Smoke Tests
                  spec:
                    type: HealthCheck
                    spec:
                      endpoints:
                        - endpoint: http://myapp-dev.example.com/health
                          method: GET
                          expectedStatus: 200
                          timeout: 30
    
    # Stage 4: 배포 (Prod - Canary)
    - stage:
        name: Deploy to Production (Canary)
        identifier: deploy_prod_canary_stage
        type: Deployment
        when:
          stageStatus: Success
          condition: <+pipeline.triggeredBy.branch> == "main"
        spec:
          deploymentType: Kubernetes
          service:
            serviceRef: myapp_service
            serviceInputs:
              - name: namespace
                value: production
          environment:
            environmentRef: prod_environment
          infrastructure:
            infrastructureDefinition:
              type: KubernetesDirect
              spec:
                connectorRef: k8s_prod_cluster
          execution:
            steps:
              # Canary 배포 (5%)
              - step:
                  type: Canary
                  identifier: canaryDeploy
                  name: Canary Deployment (5% traffic)
                  spec:
                    instances:
                      type: Count
                      value: 1
                    traffic:
                      weight: 5
              
              # 헬스 검증
              - step:
                  type: VerifyDeployment
                  identifier: verifyCanary
                  name: Verify Canary Health
                  spec:
                    type: PrometheusMetrics
                    prometheus:
                      metricQuery: |
                        rate(http_requests_total{status=~"5.."}[5m])
                      operator: LessThan
                      threshold: 0.01  # 1% 미만 에러율
              
              # 트래픽 점진 증가
              - step:
                  type: Traffic
                  identifier: increaseTraffic50
                  name: Shift to 50% traffic
                  spec:
                    weight: 50
              
              - step:
                  type: Traffic
                  identifier: increaseTraffic100
                  name: Shift to 100% traffic
                  spec:
                    weight: 100
              
              # 최종 검증
              - step:
                  type: VerifyDeployment
                  identifier: verifyProduction
                  name: Verify Production Stability
                  spec:
                    type: DatadogMetrics
                    datadog:
                      queries:
                        - metricPath: "avg:trace.web.request.duration"
                          operator: LessThan
                          threshold: 500

  variables:
    - name: BUILD_NUMBER
      value: <+pipeline.execution.number>
    - name: GIT_COMMIT
      value: <+pipeline.triggeredBy.commit>

  notifications:
    - channel:
        type: Slack
        spec:
          webhookUrl: <+secrets.getValue("slack_webhook")>
      events:
        - type: PipelineExecutionSuccess
        - type: PipelineExecutionFailure
```

### 3.2 Harness Feature Flags

```yaml
# .harness/feature-flags.yaml
---
# Feature Flag: 새로운 결제 UI
kind: FeatureFlag
metadata:
  name: new_payment_ui
  namespace: myapp
spec:
  description: "새로운 결제 인터페이스 롤아웃"
  type: boolean
  default: false
  targets:
    - name: internal_team
      percentage: 100
    - name: beta_users
      percentage: 50
    - name: external_users
      percentage: 0
  rules:
    - condition: user.email contains "@company.com"
      variation: true
    - condition: user.plan == "premium"
      variation: true
      percentage: 20

---
# Feature Flag: 결제 재시도 로직
kind: FeatureFlag
metadata:
  name: payment_retry_v2
  namespace: myapp
spec:
  description: "개선된 결제 재시도 로직"
  type: boolean
  default: false
  multivariate: false
```

---

## 4. 성능 및 부하 테스트 하네스

### 4.1 k6를 사용한 부하 테스트

```javascript
// tests/load/checkout_load_test.js
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate, Trend, Counter, Gauge } from 'k6/metrics';

// 커스텀 메트릭
const errorRate = new Rate('errors');
const checkoutDuration = new Trend('checkout_duration');
const activeUsers = new Gauge('active_users');

export const options = {
  stages: [
    { duration: '1m', target: 10 },   // 1분에 10명으로 증가
    { duration: '5m', target: 50 },   // 5분 동안 50명 유지
    { duration: '1m', target: 100 },  // 1분에 100명으로 증가
    { duration: '5m', target: 100 },  // 5분 동안 100명 유지
    { duration: '1m', target: 0 },    // 1분에 0명으로 감소
  ],
  thresholds: {
    'errors': ['rate<0.1'],              // 에러율 10% 미만
    'checkout_duration': ['p(95)<2000'], // 95 percentile < 2초
    'http_req_duration': ['p(99)<3000'],
  },
};

const BASE_URL = 'http://localhost:8000';
let userCounter = 0;

export default function() {
  const userId = ++userCounter;
  
  // Active users 업데이트
  activeUsers.add(1);
  
  group('User Registration', () => {
    const registerRes = http.post(
      `${BASE_URL}/api/auth/register`,
      JSON.stringify({
        email: `user${userId}@example.com`,
        password: 'password123',
        name: `User ${userId}`,
      }),
      {
        headers: { 'Content-Type': 'application/json' },
      }
    );
    
    check(registerRes, {
      'registration status 201': (r) => r.status === 201,
      'registration has token': (r) => r.json('token') !== undefined,
    }) || errorRate.add(1);
  });
  
  sleep(1);
  
  group('Add to Cart', () => {
    const addToCartRes = http.post(
      `${BASE_URL}/api/cart/items`,
      JSON.stringify({
        productId: 'product_1',
        quantity: 2,
      }),
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer token_${userId}`,
        },
      }
    );
    
    check(addToCartRes, {
      'add to cart 200': (r) => r.status === 200,
    }) || errorRate.add(1);
  });
  
  sleep(2);
  
  group('Checkout', () => {
    const startTime = new Date();
    
    const checkoutRes = http.post(
      `${BASE_URL}/api/checkout`,
      JSON.stringify({
        paymentMethod: 'credit_card',
        cardToken: 'tok_visa',
      }),
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer token_${userId}`,
        },
      }
    );
    
    const duration = new Date() - startTime;
    checkoutDuration.add(duration);
    
    check(checkoutRes, {
      'checkout status 200': (r) => r.status === 200,
      'checkout response time < 2s': (r) => r.timings.duration < 2000,
      'checkout has order id': (r) => r.json('orderId') !== undefined,
    }) || errorRate.add(1);
  });
  
  activeUsers.add(-1);
  sleep(5);
}

export function teardown(data) {
  console.log(`Test completed. Total users: ${userCounter}`);
}
```

### 4.2 성능 테스트 해석

```bash
# k6 실행
k6 run tests/load/checkout_load_test.js

# 결과 분석 예시:
# errors ......................... 4.50% ✓ (< 10%)
# checkout_duration ............. avg=1234ms p(95)=1890ms ✓ (< 2000ms)
# http_req_duration ............. avg=456ms p(99)=2834ms ✓ (< 3000ms)
```

---

## 5. AI 기반 테스트 생성

### 5.1 Claude를 사용한 테스트 생성

```python
# tests/ai_generated/test_generator.py
from anthropic import Anthropic

class AITestGenerator:
    """Claude를 사용한 테스트 자동 생성"""
    
    def __init__(self, api_key):
        self.client = Anthropic(api_key=api_key)
    
    def generate_tests_from_code(self, code_snippet: str) -> str:
        """코드에서 테스트 생성"""
        
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": f"""
다음 Python 함수에 대해 포괄적인 pytest 테스트를 생성해주세요.
테스트는 다음을 포함해야 합니다:
1. 정상 케이스
2. 엣지 케이스
3. 예외 처리
4. 입력 검증

함수:
```python
{code_snippet}
```

테스트 코드만 제공하세요 (설명 제외).
"""
                }
            ]
        )
        
        return message.content[0].text
    
    def generate_tests_from_requirements(self, requirements: str) -> str:
        """요구사항에서 테스트 생성"""
        
        message = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=3000,
            messages=[
                {
                    "role": "user",
                    "content": f"""
다음 요구사항에 대해 pytest 테스트 스위트를 생성해주세요:

{requirements}

테스트는:
- fixtures를 활용하기
- Mock을 적절히 사용하기
- 명확한 assertion 사용하기
- 테스트 이름이 명확하기
- conftest.py 형식 활용하기

생성된 테스트 코드를 반환해주세요.
"""
                }
            ]
        )
        
        return message.content[0].text


# 사용 예제
if __name__ == "__main__":
    import os
    
    generator = AITestGenerator(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # 1. 함수에서 테스트 생성
    code = """
def calculate_discount(price: float, customer_type: str) -> float:
    if customer_type == "premium":
        discount = price * 0.2
    elif customer_type == "regular":
        discount = price * 0.1
    else:
        discount = 0
    return price - discount
    """
    
    tests = generator.generate_tests_from_code(code)
    print("Generated Tests:")
    print(tests)
    
    # 2. 요구사항에서 테스트 생성
    requirements = """
사용자 인증 기능:
- 유효한 이메일과 비밀번호로 로그인
- 유효하지 않은 이메일로 로그인 시 실패
- 존재하지 않는 사용자 처리
- 비밀번호 재시도 3회 실패 시 잠금
- 토큰 만료 처리
    """
    
    tests = generator.generate_tests_from_requirements(requirements)
    print("\nGenerated Tests from Requirements:")
    print(tests)
```

---

## 마무리

이 예제들은 실제 프로덕션 환경에서 사용할 수 있는 테스트 하네스 패턴을 보여줍니다.
핵심은 **재사용 가능하고, 유지보수하기 쉽고, 빠른 피드백**을 제공하는 구조입니다.

