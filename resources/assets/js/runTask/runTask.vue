<template>
  <div class="run-task col-lg-6">
    <div class="card">
      <div class="card-header">
        Запуск задачи
      </div>
      <div class="card-body">

        <table class="table">
          <tr>
            <td>Название задачи</td>
            <td>
              <input
                type="text"
                class="form-control"
                v-model="task_name">
            </td>
          </tr>

          <tr>
            <td>Параметры</td>
            <td>
              <input
                type="text"
                class="form-control"
                v-model="params">
            </td>
          </tr>

          <tr>
            <td>Email</td>
            <td>
              <input
                type="text"
                class="form-control"
                v-model="email">

            </td>
          </tr>

          <tr>
            <td colspan="2">

               <button
                 @click="runTask()"
                 class="btn btn-success pull-right">

                 Выполнить
               </button>
            </td>
          </tr>
        </table>
      </div>
    </div>

      <div
        v-if="error && error.length"
        class="alert alert-danger">

          {{ error }}
      </div>

      <div
        v-if="result && result.length"
        class="results-block card">

        <div class="card-header">
          Результат выполнения задачи
        </div>

        <div class="card-body">
           <textarea
                v-model="result"
                class="form-control">
           </textarea>
        </div>
      </div>
  </div>
</template>

<script>

  import axios from 'axios';

  export default {
    data() {
      return {
        task_name: '',
        params: '',
        email: '',
        result: '',
        error: ''
      }
    },
    methods: {
      runTask() {
        let params = {
          task_name: this.task_name,
          params: this.params,
          email: this.email
        };

        axios
        .post("/run_task", params)
        .then(response => {

          if (!response || !response.data) {

            this.error = 'Ошибка получения данных с сервера';
            this.result = '';
            return;
          }

          if (response.data.error) {
            this.result = '';
            this.error = response.data.error.error_msg;
            return;
          }

          this.result = response.data.result;
          this.error = '';

        }).catch(error => {

          this.result = '';
          this.error = error;
        });
      }
    },
    components: {}
  }
</script>