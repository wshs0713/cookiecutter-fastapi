import uvicorn
from core.registers import FastAPIRegister

registry = FastAPIRegister()
app = registry.create_app()


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level='info',
        forwarded_allow_ips='*'
    )
