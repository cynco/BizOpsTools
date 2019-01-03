from flask import Flask
from flask import render_template, request, make_response, send_file
from werkzeug import secure_filename
from convert import converter
from flask_cors import CORS
import os
app = Flask(__name__)

# create the folders when setting up your app
os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)



poll_data = {
   'question' : 'Select the file type (choose one)',
   'fields'   : ['1. OpenTable Reservation Report', '2. OpenTable Guestcenter Export'
   , '3. OpenTable Guestcenter Guestbook', '4. OpenTable Terminal Guestbook']
}
pollfilename = 'data.txt'
 
@app.route('/')
def root():
    return render_template('poll.html', data=poll_data)

# @app.route('/poll')
# def poll():
#     vote = request.args.get('field')
#     out = open(pollfilename, 'w')
#     out = open(pollfilename, 'a')
#     print("check if file created")
#     out.write( vote + '\n' )
#     out.close()
# #     return render_template('thankyou.html', data=poll_data)
# # example from https://code-maven.com/a-polling-station-with-flask
#     return vote 


@app.route('/upload')
def upload_file1():
      vote = request.args.get('field')
      out = open(pollfilename, 'w')
      # out = open(pollfilename, 'a')
      print("check if file created")
      out.write( vote + '\n' )
      out.close()
      return render_template('upload.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
      pollf  = open(pollfilename, 'r')
      for line in pollf:
        vote = line.rstrip("\n")
        print("vote=",vote)
      if request.method == 'POST':
            if vote == "1. OpenTable Reservation Report":
                  print("OpenTable Reservation Report type file")
                  if 'reservation_file' not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                  f = request.files['reservation_file']
                  nameOfFile = os.path.join(app.instance_path, 'htmlfi', secure_filename(f.filename))
                  print("file name: ", nameOfFile, f)
                  f.save(nameOfFile)
                  dfr = converter(nameOfFile)
                  print(dfr.shape)
                  print('RESERVATION_FILE')
                  # give unique filenames
                  csv = dfr.to_csv('OpenTable_Reservation_Report.csv')
                  # try:
                  #       return send_file('OpenTable_Reservation_Report.csv', attachment_filename='OpenTable_Reservation_Report.csv')
                  # except Exception as ex:
                  #       return str(ex)
            else:
                  return "File type mismatch"
            # print('file converted successfully')

            try:
            # return send_file('OpenTable_Reservation_Report.csv', attachment_filename='reformatted_reservation_report.csv')
                  CORS(app, expose_headers=["x-suggested-filename"])

            # In file with the download endpoint
                  result = send_file("Reformatted_Reservation_Report.csv",
                        mimetype="text/csv",
                        as_attachment=True,
                        conditional=False)
                  result.headers["x-suggested-filename"] = "use_this_filename.csv"  # not showing this name
                  return result
            except Exception as e:
                  return str(e)
      return render_template('thankyou.html')

@app.route('/return')
def return_files_tut():
      try:
            # return send_file('OpenTable_Reservation_Report.csv', attachment_filename='reformatted_reservation_report.csv')
            CORS(app, expose_headers=["x-suggested-filename"])

            # In file with the download endpoint
            result = send_file("OpenTable_Reservation_Report.csv",
                   mimetype="text/csv",
                   as_attachment=True,
                   conditional=False)
            result.headers["x-suggested-filename"] = "use_this_filename.csv"
            return result
      except Exception as e:
            return str(e)


# Allow user to upload multiple files at once as logn as they're of the same type
# improve using http://flask.pocoo.org/docs/1.0/patterns/fileuploads/#uploading-files

# @app.route('/converter')
# def convert():
#     newfile = converter(filename)
#     return 'newfile'

# response = make_response(csv)
# cd = 'attachment; filename=EsinFutureResos.csv'
# response.headers['Content-Disposition'] = cd
# response.mimetype='text/csv'
# return response

if __name__ == '__main__':
   app.run()
