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
        class="error-block alert alert-danger">

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
        task_name: 'multiprint',
        params: '{"msg": "hello", "count": 3}',
        email: '',
        result: '',
        error: ''
      }
    },
    methods: {
      runTask() {

        if (this.email && this.email.length >0) {
          var re = /\S+@\S+\.\S+/;
          if (!re.test(this.email)) {
            alert("Введите корректный email");
            return;
          }
        }

        let params = {
          task_name: this.task_name,
          params: this.params,
          email: this.email
        };

        try {
          axios
          .post("/run_task", params)
          .then(response => {

          this.result = '';
          this.error = '';

          if (!response || !response.data) {

            this.error = 'Ошибка получения данных с сервера';
            return;
          }

          if (response.data.status
              && response.data.status == 'ERROR') {

            this.error = response.data.error_msg;
            return;
          }

          if (response.data.status
              && response.data.status == 'OK') {

            this.result = response.data.status;
          } else {

            this.result = response.data.result;
          }

          }).catch(error => {

            this.result = '';
            this.error = 'Ошибка получения данных с сервера';
          });

        } catch(e) {
          this.result = '';
          this.error = 'Ошибка получения данных с сервера';
        }
      }
    },
    components: {}
  }
</script>