# Contribuindo para Wizarding Duel

Obrigado pelo interesse em contribuir para o projeto Wizarding Duel! Este documento contém diretrizes para contribuições.

## Como Contribuir

### Reportando Bugs

1. Verifique se o bug já foi reportado nas [Issues](https://github.com/anderson-ufrj/project-game-py/issues)
2. Se não foi reportado, crie uma nova issue com:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Screenshots se aplicável
   - Informações do sistema (SO, versão do Python, etc.)

### Sugerindo Melhorias

1. Verifique se a sugestão já existe nas Issues
2. Crie uma nova issue marcada como "enhancement" com:
   - Descrição detalhada da funcionalidade
   - Justificativa para a mudança
   - Exemplos de uso se aplicável

### Contribuindo com Código

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça suas mudanças seguindo as diretrizes de código
4. Teste suas mudanças
5. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
6. Push para a branch (`git push origin feature/nova-funcionalidade`)
7. Abra um Pull Request

## Diretrizes de Código

### Estilo de Código

- Siga a PEP 8 para estilo Python
- Use nomes de variáveis descritivos em português
- Comente código complexo
- Mantenha funções pequenas e focadas

### Estrutura de Commits

Use mensagens de commit claras e descritivas:
```
tipo: breve descrição

Descrição mais detalhada se necessário

- Lista de mudanças específicas
- Outras mudanças relevantes
```

Tipos de commit:
- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: mudanças na documentação
- `style`: formatação, ponto e vírgula faltando, etc
- `refactor`: refatoração de código
- `test`: adição ou correção de testes
- `chore`: mudanças de build, aux tools, etc

### Testando

Antes de enviar um PR:
1. Execute o jogo e verifique se funciona corretamente
2. Teste as funcionalidades modificadas
3. Verifique se não quebrou funcionalidades existentes

## Configuração do Ambiente de Desenvolvimento

1. Clone o repositório:
   ```bash
   git clone git@github.com:anderson-ufrj/project-game-py.git
   cd project-game-py
   ```

2. Execute o script de configuração:
   ```bash
   ./run.sh
   ```

3. Para desenvolvimento, ative o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```

## Áreas que Precisam de Ajuda

- [ ] Mais tipos de varinhas e diabretes
- [ ] Sistema de power-ups
- [ ] Melhores efeitos visuais
- [ ] Sistema de salvamento de high scores
- [ ] Música e efeitos sonoros melhorados
- [ ] Testes automatizados
- [ ] Suporte a outros sistemas operacionais
- [ ] Modos de jogo alternativos

## Perguntas?

Se tiver dúvidas, abra uma issue ou entre em contato através do GitHub.

Obrigado por contribuir! 🚀