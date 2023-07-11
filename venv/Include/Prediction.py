class Prediction:
    open = True
    default_answers = ["yes", "no"]
    current_question = "question"
    current_answers = []
    winning_prediction = ""
    ans_delimiter = "/:/"
    user_prediction = {}
    point_name = "channel points"
    pool = 0
    user_creator = 0

    def reset_poll(self):
        self.open = True
        self.default_answers = ["yes", "no"]
        self.current_question = "question"
        self.current_answers = []
        self.user_prediction = {}
        self.pool = 0

    # takes in question as a string and can also take in a List of answers
    def __init__(self, question="question", answer=default_answers):
        self.reset_poll()
        self.current_question = question
        self.current_answers = answer

    def parse_poll(self, input_string):
        quest = ""
        ans = []
        param = input_string.replace('!poll', '')
        param = param.strip()
        if param.find(self.ans_delimiter) != -1:
            param = param.split(self.ans_delimiter)
            if len(param) > 1:
                quest = param[0]
                ans = param[1:len(param)]
        else:
            quest = param
            ans = self.default_answers
        self.current_answers = ans
        self.current_question = quest

        # print(quest + ":" + str(ans))

    def close_prediction(self):
        self.open = False

    def open_prediction(self):
        self.open = True

    def set_delimiter(self, delimiter="/:/"):
        self.ans_delimiter = delimiter

    def check_valid_prediction(self, prediction):
        if prediction in self.current_answers:
            return True
        else:
            return False

    def add_user_prediction(self, user, prediction, prediction_amount):
        tmp_val = 0
        if self.check_valid_prediction(prediction):
            if user in self.user_prediction:
                tmp_val = self.user_prediction[user][1]
                self.user_prediction[user] = [prediction, prediction_amount + tmp_val]
            else:
                self.user_prediction[user] = [prediction, prediction_amount]
            return True
        else:
            return False

    def clear_predictions(self):
        self.user_prediction.clear()

    def _update_pool(self):
        tmp = 0
        for v in self.user_prediction.values():
            tmp += v[1]
        self.pool = tmp
        return tmp

    def get_pool(self):
        return self._update_pool()

    # returns a dictionary consisting of users who predicted a certain outcome
    # and amount predicted
    def get_prediction_users(self, prediction):
        user = {}
        amount = 0
        tmp = 0
        for p in self.user_prediction.items():
            if p[1][0] == prediction:
                tmp = p[1][1]
                user[p[0]] = tmp
                amount += tmp
        return user

    def get_prediction_totals(self, prediction):
        amount = 0
        count = 0
        tmp = 0
        for p in self.user_prediction.items():
            if p[1][0] == prediction:
                tmp = p[1][1]
                amount += tmp
                count += 1
        return [amount, count]

    # returns dictionary of winners and amount for each
    def get_winners(self, winning_prediction):
        payout = {}
        pool = self.get_pool()
        wager = 0
        pay_total = 0
        tmp_percent = 0
        winner_pool = self.get_prediction_totals(winning_prediction)[0]
        winner_count = self.get_prediction_totals(winning_prediction)[1]
        winners = self.get_prediction_users(winning_prediction)
        for w in winners:
            wager = winners[w]
            tmp_percent = wager / winner_pool
            pay_total = round(tmp_percent * pool, 2)
            payout[w] = pay_total
            print(w + ":" + str(round(tmp_percent * 100, 2)))
        return payout
        # print(str(winners))

    def get_split_totals(self):
        predictions = {}
        for p in self.current_answers:
            predictions[p] = self.get_prediction_totals(p)[0]
        return predictions

    def get_split_totals_user_count(self):
        predictions = {}
        for p in self.current_answers:
            predictions[p] = self.get_prediction_totals(p)
        return predictions

    # dictionary of user predictions with prediction as primary key
    def get_split_users(self):
        predictions = {}
        for p in self.current_answers:
            predictions[p] = self.get_prediction_users(p)
        return predictions

    def __str__(self):
        return self.current_question + ":" + str(self.current_answers)


if __name__ == '__main__':
    test_str = "will we win? /:/yes /:/no /:/maybe"
    test_str2 = "will we win AGAIN?"
    test_str3 = "will we win? /-/yes /-/no"
    p = Prediction()
    p.parse_poll(test_str2)
    p.add_user_prediction("bob", "yes", 500)
    p.add_user_prediction("bill", "yes", 1000)
    p.add_user_prediction("bell", "no", 450)
    p.add_user_prediction("larry", "maybe", 5000)
    print(str(p.get_split_totals()))
    print(str(p.get_prediction_users("yes")))
    print(str(p.get_winners("yes")))
    print(str(p.get_winners("no")))
