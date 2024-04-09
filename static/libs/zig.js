// Vue.http.options.emulateJSON = true;
new Vue({
    el: '#app',
    delimiters:['_%','%_'],
    data() {
        return {
          continue_time : false,
          data_headers:[],
          tableData: [{
            
          }],
          retData :[],
          isdrawershow:false,
          freq: 'D',
          value: '',
          date_start: '2024-01-01 10:10:10',
          num: "10",
          data_cols:"",
          data_rows:""
        }
      },
      methods: {
        handleInputCol(val){
            this.tableData.length=0;
            fields = val.split(",")
            for(f in fields){
                this.tableData.push({"label":fields[f] , "prop" :fields[f] , "name" :fields[f] , "func": "F_EMPTY"});
            }
            // console.log(this.data_headers)
        },


        reset(){
            this.retData = [];
            this.tableData = [{}];
            this.data_cols = "";
        },

        showRet(){
          this.isdrawershow = true;
        },

        apply(){
            var args = {}
            args['data_conf'] = this.tableData;
            args['date_start']  = this.date_start;
            args['data_rows'] = this.data_rows;
            args['freq'] = this.freq;
            this.$http.post("/apply" , args).then(result => {
              
              console.log("====" , result);
              this.retData.push(result.body);
              // console.log("====" , result);
              this.isdrawershow = true;
          });
        },

        downloads(){
          var header = this.data_cols.split(",")
          // console.log("=====" , this.tableData)
          // for(item in this.tableData){
          //   header.push(item['name']);
          // }

          var para = {};
          para["header"] = header;
          para['data'] = this.retData;

          this.$http.post("/export",para).then(res => {
            // console.log(res)
            let blob = new Blob([res.body])
            let reader = new FileReader()
            reader.readAsDataURL(blob)
            reader.onload = (e) => {
              let a = document.createElement('a')
              /* 默认文件名 */
              a.download = 'result.csv';
              a.href = e.target.result
              document.body.appendChild(a)
              a.click()
              document.body.removeChild(a)
              // this.onClose()
            }
          });
        }
      }
      
})