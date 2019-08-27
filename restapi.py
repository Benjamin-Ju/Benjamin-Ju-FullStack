from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify

import psycopg2
import datetime as dt
from flask_cors import CORS

connection = psycopg2.connect(user = "postgres",
                              password = "chicken!1",
                              host = "localhost",
                              port = "5432",
                              database = "benjamin-ju")
cursor = connection.cursor()

db_connect = create_engine('postgresql://postgres:chicken!1@localhost:5432/benjamin-ju')
conn = db_connect.connect()
app = Flask(__name__)
CORS(app)
api = Api(app)

class DayActivityLog(Resource):
    def get(self, date):
        cursor.execute(
            """
            SELECT start_time, end_time, activity
            FROM activity_log WHERE date = '{}'
            """.format(date)
        )
        activities = cursor.fetchall()
        log = []
        for activity in activities:
            start_time = activity[0].strftime("%I:%M%p")
            end_time = activity[1].strftime("%I:%M%p")
            log.append(start_time + " - " + end_time + " " + activity[2])

        return {date: log}

class DayExpenseLog(Resource):
    def get(self, date):
        cursor.execute(
            """
            SELECT expense, value
            FROM expenses WHERE date = '{}'
            """.format(date)
        )
        expenses = cursor.fetchall()
        log = []
        for expense in expenses:
            log.append("$" + str(expense[1]) + " - " + expense[0])

        return {date: log}


api.add_resource(DayActivityLog, '/day_activity_log/<date>')
api.add_resource(DayExpenseLog, '/day_expense_log/<date>')

if __name__ == '__main__':
    app.run(port='5002')