# pantapalabras
pantapalabras is a FastAPI backend service.

### Steps to run locally:
1. Move to the pantapalabras directory.
   ```shell
   $ cd pantapalabras
   ```

2. Create virtualenv and activate it.
   ```shell
   $ virtualenv venv -p python3
   $ . venv/bin/activate
   ```

3. Install requirements.
    ```shell
   $ pip install -r requirements.txt
   ```

4. Run:
    ```shell
   $ uvicorn pantapalabras.api:app --port=9173 --host=0.0.0.0 --reload
   ```
