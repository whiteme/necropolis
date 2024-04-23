// Vue.http.options.emulateJSON = true;
new Vue({
    el: '#app',
    delimiters:['_%','%_'],
    data() {
        return {
          centerDialogVisible : false, // see all dialog flag
          continue_time : false, // time set switch
          data_headers:[],
          tableData: [{}], // column configs
          retData :[],// temp result [[0][...] , [1][...],...]
          totalData:[],//for see all
          isdrawershow:false, // temp result drawer flag
          freq: 'MIN', //time unit
          step: 1, //time step
          value: '',
          date_start: '2024-01-01 10:10:10', // time val
          num: "10",
          data_cols:"", // header input
          data_cols_disabled:false, // header input editable
          data_rows: 1 // summon rows
        }
      },
      computed:{
        arraySum() {
          return this.retData.reduce((sum, item) => sum + item.length, 0);
        },
      },

      methods: {
        //handle column input change event
        handleInputCol(val){
            this.tableData.length=0;
            fields = val.split(",")
            for(f in fields){
                this.tableData.push({"label":fields[f] , "prop" :fields[f] , "name" :fields[f] , "func": "F_EMPTY"});
            }
            // console.log(this.data_headers)
        },

        // reset btn click
        reset(){
            this.retData = [];
            this.tableData = [{}];
            this.data_cols = "";
            this.data_cols_disabled = false;
        },
        // dispel btn click
        dropData(){
          this.retData = [];
        },

        // check btn click
        showRet(){
          this.isdrawershow = true;
        },

        //time switch on change 
        changeST(){
          if(this.continue_time){
            this.extend_time();
          }
        },

        // format js Date to Str "yyyy-MM-dd HH:mm:ss"
        formatDate(date) {
          const year = date.getFullYear();
          const month = String(date.getMonth() + 1).padStart(2, '0');
          const day = String(date.getDate()).padStart(2, '0');
          const hours = String(date.getHours()).padStart(2, '0');
          const minutes = String(date.getMinutes()).padStart(2, '0');
          const seconds = String(date.getSeconds()).padStart(2, '0');
          return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        },

        //set st for lastes records timestamp
        extend_time(){
           var target = "2000-01-01 00:00:00";
           for(var i=0;i<this.retData.length;i++){
              var batch = this.retData[i];
              for(var j = 0 ; j<batch.length;j++){
                var item = batch[j];
                if(item['index'] > target){
                  target = item['index']
                }
              }
           }
          
           
           var currentDate = new Date(target);
          //  console.log("=", currentDate , this.freq)
           if(this.freq =="H"){
            currentDate = new Date(currentDate.setHours(currentDate.getHours() + 1));
           }else if(this.freq =="MIN"){
            currentDate = new Date(currentDate.setMinutes(currentDate.getMinutes() + 1));
           }else if(this.freq =="S"){
            currentDate = new Date(currentDate.setSeconds(currentDate.getSeconds() + 1));
           }else if(this.freq =="D"){
            currentDate = new Date(currentDate.setDate(currentDate.getDay() + 1));
           }
          //  console.log("==", currentDate , this.freq)
           this.date_start = this.formatDate(currentDate);

        },

        
        //summon
        apply(){

            if(this.data_rows <1 || this.data_cols == ""){

              this.$notify({
                title: 'Failed to Summon CSV',
                message: 'Set right headers and row nums PLZ!',
                type: 'warning',
                offset:40,
                position: 'top-left'
              });
              return;
            }
            
            var args = {}
            args['data_conf'] = this.tableData;
            args['date_start']  = this.date_start;
            args['data_rows'] = this.data_rows;
            args['freq'] =this.step +  this.freq;
            this.$http.post("/apply" , args).then(result => {
              this.data_cols_disabled = true;
              // console.log("====" , result);
              this.retData.push(result.body);
              // console.log("====" , result);
             
              if(this.continue_time){
                this.extend_time();
              }
              
              this.isdrawershow = true;
              
              this.$message({
                title: 'Summon Success',
                message: 'Summon Success',
                type: 'success',
                customClass:'messageIndex'
              } );
              
             
             
          });
        },

        // delete batch data on temp ret drawer
        del_item(index){
            // console.log("======",e)
            this.retData.splice(index , 1);
            this.$notify({
              title: "Done",
              message: 'Delete Batch   [' + (index+1) + "]    Data Successful",
              type: 'success',
              offset:40,
              position: 'top-left'
            });
        },
        //export 2 csv
        downloads(){

          if(this.retData.length < 1){
            this.$notify({
              title: 'Failed to Export CSV File',
              message: 'Empty result,Summon it first',
              type: 'warning',
              offset:40,
              position: 'top-left'
            });
            return;
          }
          var header = this.data_cols.split(",")

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
        },
        // see all btn click
        showPreview(){
          this.centerDialogVisible = true;
          this.totalData = []
          for(var i=0;i<this.retData.length;i++){
            var batch = this.retData[i];
            for(var j = 0 ; j<batch.length;j++){
              var item = batch[j];
              item['batch'] = i+1;
              this.totalData.push(item);
            }
         }
         this.totalData.sort((a, b) => new Date(a['index']).getTime()  - new Date(b['index']).getTime())
        },

        // set diff batch for diff bg-color
        tableRowClassName(para){
            // return "r"+row['batch']%10;
            return "r"+ (para['row']['batch']%10);
        }
      }
})