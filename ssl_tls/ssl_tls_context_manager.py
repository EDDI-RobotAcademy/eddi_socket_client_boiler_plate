import ssl


class SslTlsContextManager:
    __sslContext = None

    @staticmethod
    def setupSSLContext(certfile, keyfile, cafile):
        if SslTlsContextManager.__sslContext is None:
            SslTlsContextManager.__sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            SslTlsContextManager.__sslContext.load_cert_chain(certfile=certfile, keyfile=keyfile)

            SslTlsContextManager.__sslContext.verify_mode = ssl.CERT_REQUIRED
            SslTlsContextManager.__sslContext.load_verify_locations(cafile=cafile)
        else:
            raise RuntimeError("SSL/TLS context is already set up.")

    @staticmethod
    def getSSLContext():
        if SslTlsContextManager.__sslContext is None:
            raise RuntimeError("SSL/TLS context has not been set up yet.")
        return SslTlsContextManager.__sslContext

    @staticmethod
    def initSslTlsContext():
        from decouple import config  # 환경 변수 로드
        # 환경 변수에서 인증서와 키 파일 경로 로드
        clientCertificate = config('CLIENT_CERTIFICATE')
        clientKey = config('CLIENT_PRIVATE')
        serverCA = config('SERVER_CA_CERTIFICATE')

        if not clientCertificate or not clientKey or not serverCA:
            raise ValueError("SSL/TLS 설정에 필요한 환경 변수가 누락되었습니다.")

        SslTlsContextManager.setupSSLContext(certfile=clientCertificate, keyfile=clientKey, cafile=serverCA)
        print("SSL/TLS context initialized successfully.")
