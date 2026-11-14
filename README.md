# Volto Light Theme Skills

Coleção de *Agent Skills* para desenvolvimento em **Plone 6**, **Volto** e **Volto Light Theme** (`@kitconcept/volto-light-theme` / `sc-volto-light-theme` / `@portalbrasil/intranet`), reunindo boas práticas de arquitetura de addons, tokens semânticos, React/TypeScript e acessibilidade.

## Skills incluídas

| Skill | Descrição |
| :--- | :--- |
| [`volto-light-theme`](skills/volto-light-theme/SKILL.md) | Regras para projetos baseados em Volto Light Theme: escada de customização (tokens → slots → registry → shadowing por último), padrões de blocos/variações, mixins, tokens semânticos e script de verificação (`check_vlt_conventions.py`). |
| [`plone-expert-developer`](skills/plone-expert-developer/SKILL.md) | Guia especializado para Plone 6 (backend Python/Dexterity/`plone.restapi`, Volto TypeScript e Classic UI). |
| [`react-best-practices`](skills/react-best-practices/SKILL.md) | Otimização de performance e padrões React da Vercel Engineering. |
| [`composition-patterns`](skills/composition-patterns/SKILL.md) | Padrões escaláveis de composição em React (compound components, providers, evita proliferação de props booleanas). |
| [`react-doctor`](skills/react-doctor/SKILL.md) | Triagem e diagnóstico de código React (lint, acessibilidade, bundle size e arquitetura). |
| [`accessibility-audit`](skills/accessibility-audit/SKILL.md) | Auditoria de acessibilidade (WCAG / axe) com evidências determinísticas. |
| [`accessible-component-review`](skills/accessible-component-review/SKILL.md) | Revisão de semântica nativa, teclado, foco, contraste e anúncios ARIA em componentes de UI. |
| [`web-design-guidelines`](skills/web-design-guidelines/SKILL.md) | Revisão de interface e UX contra diretrizes de Web Interface Guidelines. |

## Como instalar

Após publicar este repositório (por exemplo, no GitHub):

```bash
npx skills add https://github.com/<seu-usuario>/volto-light-theme-skills
```

Ou localmente (copiando ou criando symlink para o diretório de skills do seu agente, como `~/.gemini/config/skills/`):

```bash
ln -s ~/volto-light-theme-skills/skills/volto-light-theme ~/.gemini/config/skills/volto-light-theme
```

## Verificação automática (VLT)

Execute o script incluído para garantir ausência de imports de `semantic-ui-react` e seletores `.ui.*` no seu addon:

```bash
python3 skills/volto-light-theme/scripts/check_vlt_conventions.py /caminho/do/projeto
```

## Créditos e Agradecimentos

Este repositório reúne e adapta conhecimentos e skills de projetos e autores da comunidade:

- **Plone & Volto**: [Plone Foundation](https://plone.org/) / [Volto](https://github.com/plone/volto) e documentação oficial (`6.docs.plone.org`).
- **Volto Light Theme**: [kitconcept GmbH](https://github.com/kitconcept/volto-light-theme) (`@kitconcept/volto-light-theme`).
- **PortalBrasil & `sc-volto-light-theme`**: [Simples Consultoria](https://github.com/simplesconsultoria) / [PortalBrasil](https://github.com/portalbrasil) (`@portalbrasil/intranet` e convenções de tokens semânticos/mixins).
- **`plone-expert-developer`**: [CodeSyntax](https://github.com/codesyntax/plone-expert-developer).
- **`react-best-practices` & `composition-patterns`**: [Vercel Engineering](https://github.com/vercel-labs/agent-skills) (licença MIT).
- **`react-doctor`**, **`accessibility-audit`**, **`accessible-component-review`** e **`web-design-guidelines`**: mantidos conforme suas respectivas licenças e metadados originais dentro de cada pasta em `skills/`.
