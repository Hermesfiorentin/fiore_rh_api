
# Fiore RH API (local)

## Como usar (Mac)

1. Abra o Terminal e navegue até a pasta descompactada:

   ```
   cd ~/Desktop/fiore_rh_api
   ```

2. Defina 3 variáveis de ambiente (copie do Supabase e OpenAI):

   ```
   export SUPA_URL="https://SEU_PROJ.supabase.co"
   export SUPA_KEY="eyJh..."
   export OPENAI_KEY="sk-..."
   ```

3. Inicie com o script:

   ```
   sh start.command
   ```

   O Terminal mostrará: *Running on http://127.0.0.1:8000*

4. Abra o navegador: <http://127.0.0.1:8000/docs>  
   Clique em **POST /pdi → Try it out** → digite

   ```json
   { "nome": "Marcela Silva" }
   ```

   e pressione **Execute** para ver o PDI.

## Publicar no Railway

1. Crie conta em railway.app (GitHub login).
2. Clique *New Project → Deploy from GitHub* e aponte para esta pasta como repositório.
3. Adicione as variáveis SUPA_URL, SUPA_KEY, OPENAI_KEY em *Variables*.
4. Railway gera uma URL pública (ex.: `https://fiore-rh.up.railway.app`).
5. Use essa URL na Action `get_pdi` do seu Custom GPT.
