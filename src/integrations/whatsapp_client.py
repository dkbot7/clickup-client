"""
Cliente WhatsApp usando Interakt API
API Documentation: https://developers.interakt.shop/
"""
import requests
import os
from typing import Optional, Dict, Any
from datetime import datetime


class InteraktWhatsAppClient:
    """
    Cliente para enviar mensagens WhatsApp via Interakt API

    Funcionalidades:
    - Enviar mensagens de texto
    - Enviar templates aprovados
    - Validar números de telefone
    - Tratamento de erros robusto

    Exemplo de uso:
        client = InteraktWhatsAppClient()
        client.send_message(
            phone="5511999999999",
            message="Olá! Sua reunião é amanhã às 10h."
        )
    """

    def __init__(self):
        """Inicializa cliente Interakt com credenciais do .env"""
        self.api_key = os.getenv("INTERAKT_API_KEY")
        self.api_url = os.getenv("INTERAKT_API_URL", "https://api.interakt.ai/v1")

        if not self.api_key:
            raise ValueError(
                "INTERAKT_API_KEY não configurado no .env. "
                "Obtenha em: https://app.interakt.shop/settings/developer-settings"
            )

        self.headers = {
            "Authorization": f"Basic {self.api_key}",
            "Content-Type": "application/json"
        }

    def _format_phone(self, phone: str) -> str:
        """
        Formata número de telefone para padrão internacional

        Args:
            phone: Número de telefone (vários formatos aceitos)

        Returns:
            Número formatado: 5511999999999

        Exemplos:
            "11999999999" -> "5511999999999"
            "+55 11 99999-9999" -> "5511999999999"
            "5511999999999" -> "5511999999999"
        """
        # Remove caracteres não numéricos
        digits = ''.join(filter(str.isdigit, phone))

        # Adiciona código do Brasil se necessário
        if len(digits) == 11:  # Só DDD + número
            digits = "55" + digits

        # Validar comprimento
        if len(digits) != 13:  # 55 + DDD (2) + número (9)
            raise ValueError(
                f"Número inválido: {phone}. "
                "Formato esperado: 5511999999999 (13 dígitos)"
            )

        return digits

    def send_message(
        self,
        phone: str,
        message: str,
        track_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Envia mensagem de texto via WhatsApp

        Args:
            phone: Número WhatsApp (formato: 5511999999999)
            message: Texto da mensagem
            track_id: ID opcional para rastreamento

        Returns:
            Response da API com status do envio

        Exemplo:
            response = client.send_message(
                phone="5511999999999",
                message="Olá! Lembrete de reunião."
            )
        """
        try:
            # Formatar telefone
            formatted_phone = self._format_phone(phone)

            # Preparar payload
            payload = {
                "countryCode": "+55",
                "phoneNumber": formatted_phone[2:],  # Remove 55
                "type": "Text",
                "data": {
                    "message": message
                }
            }

            if track_id:
                payload["callbackData"] = track_id

            # Enviar requisição
            response = requests.post(
                f"{self.api_url}/public/message/",
                headers=self.headers,
                json=payload,
                timeout=10
            )

            # Tratar resposta
            if response.status_code == 200:
                print(f"✅ WhatsApp enviado para {formatted_phone}")
                return {
                    "success": True,
                    "phone": formatted_phone,
                    "message_id": response.json().get("result", {}).get("messageId"),
                    "response": response.json()
                }
            else:
                print(f"❌ Erro ao enviar WhatsApp: {response.status_code}")
                print(f"   Resposta: {response.text}")
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }

        except ValueError as e:
            print(f"❌ Erro de validação: {e}")
            return {"success": False, "error": str(e)}

        except Exception as e:
            print(f"❌ Erro inesperado ao enviar WhatsApp: {e}")
            return {"success": False, "error": str(e)}

    def send_template(
        self,
        phone: str,
        template_name: str,
        language_code: str = "pt_BR",
        **template_params
    ) -> Dict[str, Any]:
        """
        Envia template aprovado pelo WhatsApp/Meta

        IMPORTANTE: Templates precisam ser aprovados no painel Interakt

        Args:
            phone: Número WhatsApp
            template_name: Nome do template aprovado
            language_code: Código do idioma (default: pt_BR)
            **template_params: Parâmetros do template

        Returns:
            Response da API

        Exemplo:
            # Template: "Olá {{1}}, sua reunião é {{2}}"
            client.send_template(
                phone="5511999999999",
                template_name="lembrete_reuniao",
                param1="João",
                param2="amanhã às 10h"
            )
        """
        try:
            formatted_phone = self._format_phone(phone)

            # Preparar parâmetros do template
            body_values = [
                {"type": "text", "text": str(value)}
                for value in template_params.values()
            ]

            payload = {
                "countryCode": "+55",
                "phoneNumber": formatted_phone[2:],
                "type": "Template",
                "template": {
                    "name": template_name,
                    "languageCode": language_code,
                    "bodyValues": body_values
                }
            }

            response = requests.post(
                f"{self.api_url}/public/message/",
                headers=self.headers,
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                print(f"✅ Template '{template_name}' enviado para {formatted_phone}")
                return {
                    "success": True,
                    "phone": formatted_phone,
                    "template": template_name,
                    "response": response.json()
                }
            else:
                print(f"❌ Erro ao enviar template: {response.status_code}")
                print(f"   Resposta: {response.text}")
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }

        except Exception as e:
            print(f"❌ Erro ao enviar template: {e}")
            return {"success": False, "error": str(e)}

    def validate_phone(self, phone: str) -> bool:
        """
        Valida se o número de telefone está no formato correto

        Args:
            phone: Número a validar

        Returns:
            True se válido, False caso contrário
        """
        try:
            self._format_phone(phone)
            return True
        except ValueError:
            return False


# Exemplo de uso
if __name__ == "__main__":
    # Teste básico
    client = InteraktWhatsAppClient()

    # Validar número
    test_phone = "11999999999"
    print(f"Número {test_phone} é válido? {client.validate_phone(test_phone)}")

    # Enviar mensagem de teste (comente se não quiser enviar)
    # result = client.send_message(
    #     phone="5511999999999",
    #     message="Teste de integração WhatsApp via Interakt"
    # )
    # print(result)
