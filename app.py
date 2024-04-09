import json, os , csv
from flask import Flask, request, jsonify, make_response, render_template, send_file
from graveyard.MeatWagon  import Drop_All_Corpses
from graveyard.Necromancer import Raise_dead 


app = Flask(__name__)


@app.route('/')
def The_damned_stand_ready():
    return  render_template("CorrodedLand.html")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/apply' , methods=["post"])
def apply():
    arg = request.get_json()
    # arg = jsonify(arg)
    data_conf = arg['data_conf']
    date_start = arg['date_start']
    rows = arg['data_rows']
    freq = arg['freq']
    df = Raise_dead(data_conf , date_start , freq , rows)
    print("==== ==== ==== " , df)
    df_dict = df.to_dict(orient='records')
    return json.dumps(df_dict)


@app.route('/export' , methods=["post"])
def export():
    arg = request.get_json()
    header = []
    header.append("index")
    for key in arg["header"]:
        header.append(key)
    data = arg["data"]
    csv_list = Drop_All_Corpses(header , data)
    temp_file_path = "temp_data.csv"
    with open(temp_file_path,'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(header)
        csv_writer.writerows(csv_list)
    
    def remove_temp_file(response):
        try:
            os.remove(temp_file_path)
        except Exception as e:
            app.logger.error("====Error" , str(e))
        return response

    # 通过 with 语句将临时文件发送给用户，并在下载完成后删除临时文件
    with app.open_resource(temp_file_path) as f:
        
        response = make_response(send_file(temp_file_path))
        response.headers["Content-Disposition"] = "attachment; filename={}".format("temp_data.csv")
        return remove_temp_file(response)

if __name__ == '__main__':
    app.run(debug=True)
