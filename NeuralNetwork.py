import numpy as np

def sigmoid(x):
  #  f(x) = 1 / (1 + e^(-x)) دالة السيجمويد
  return 1 / (1 + np.exp(-x))

def deriv_sigmoid(x):
  # f'(x) = f(x) * (1 - f(x)) : مشتقة السيجمويد
  fx = sigmoid(x)
  return fx * (1 - fx)

def mse_loss(y_true, y_pred):
  # بنفس الطول arrays عبارة عن  y_true و  y_pred
  return ((y_true - y_pred) ** 2).mean()

class OurNeuralNetwork:
  '''
  :الشبكة العصبية لديها
    - مدخلين
    - (h1, h2) طبقة خفية تحتوي على عصبونين
    - (o1) طبقة مخرجات تحتوي على عصبون واحد

  '''
  def __init__(self):
    # الأوزان
    self.w1 = np.random.normal()
    self.w2 = np.random.normal()
    self.w3 = np.random.normal()
    self.w4 = np.random.normal()
    self.w5 = np.random.normal()
    self.w6 = np.random.normal()

    # الإنحياز
    self.b1 = np.random.normal()
    self.b2 = np.random.normal()
    self.b3 = np.random.normal()

  def feedforward(self, x):
    # لها عنصرين array هي  x
    h1 = sigmoid(self.w1 * x[0] + self.w2 * x[1] + self.b1)
    h2 = sigmoid(self.w3 * x[0] + self.w4 * x[1] + self.b2)
    o1 = sigmoid(self.w5 * h1 + self.w6 * h2 + self.b3)
    return o1

  def train(self, data, all_y_trues):
    '''
   تساوي عدد الأمثلة n و  (n x 2) حجمها  numpy array البيانات هي
   عناصر   n لها  numpy array هي all_y_trues
    تمثل البيانات  all_y_trues العناصر في
    '''
    learn_rate = 0.1
    epochs = 1000 # عدد الدورات خلال البيانات

    for epoch in range(epochs):
      for x, y_true in zip(data, all_y_trues):
        # --- التفذية الأمامية و التي سنحتاجها لاحقاً
        sum_h1 = self.w1 * x[0] + self.w2 * x[1] + self.b1
        h1 = sigmoid(sum_h1)

        sum_h2 = self.w3 * x[0] + self.w4 * x[1] + self.b2
        h2 = sigmoid(sum_h2)

        sum_o1 = self.w5 * h1 + self.w6 * h2 + self.b3
        o1 = sigmoid(sum_o1)
        y_pred = o1

        # --- .حساب المشتقات الجزئيى
        d_L_d_ypred = -2 * (y_true - y_pred)

        # o1 العصبون
        d_ypred_d_w5 = h1 * deriv_sigmoid(sum_o1)
        d_ypred_d_w6 = h2 * deriv_sigmoid(sum_o1)
        d_ypred_d_b3 = deriv_sigmoid(sum_o1)

        d_ypred_d_h1 = self.w5 * deriv_sigmoid(sum_o1)
        d_ypred_d_h2 = self.w6 * deriv_sigmoid(sum_o1)

        # h1 العصبون
        d_h1_d_w1 = x[0] * deriv_sigmoid(sum_h1)
        d_h1_d_w2 = x[1] * deriv_sigmoid(sum_h1)
        d_h1_d_b1 = deriv_sigmoid(sum_h1)

        # h2 العصبون
        d_h2_d_w3 = x[0] * deriv_sigmoid(sum_h2)
        d_h2_d_w4 = x[1] * deriv_sigmoid(sum_h2)
        d_h2_d_b2 = deriv_sigmoid(sum_h2)

        # --- تحديث الأوزان و الإنحياز
        # h1 العصبون
        self.w1 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w1
        self.w2 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_w2
        self.b1 -= learn_rate * d_L_d_ypred * d_ypred_d_h1 * d_h1_d_b1

        # h2 العصبون
        self.w3 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_w3
        self.w4 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_w4
        self.b2 -= learn_rate * d_L_d_ypred * d_ypred_d_h2 * d_h2_d_b2

        # O1 العصبون
        self.w5 -= learn_rate * d_L_d_ypred * d_ypred_d_w5
        self.w6 -= learn_rate * d_L_d_ypred * d_ypred_d_w6
        self.b3 -= learn_rate * d_L_d_ypred * d_ypred_d_b3

      # --- epoch حساب الخسارة بعد كل
      if epoch % 10 == 0:
        y_preds = np.apply_along_axis(self.feedforward, 1, data)
        loss = mse_loss(all_y_trues, y_preds)
        print("Epoch %d loss: %.3f" % (epoch, loss))

# التغريف بالبيانات
data = np.array([
  [-2, -1],  # إيمان
  [25, 6],   # مدثر
  [17, 4],   # عبد الفتاح
  [-15, -6], # أمال
])
all_y_trues = np.array([
  1, # إيمان
  0, # مدثر
  0, # عبد الفتاح
  1, # أمال
])

# تدريب الشبكة العصبية
network = OurNeuralNetwork()
network.train(data, all_y_trues)
# القيام بالتنبؤ
Hala = np.array([-7, -3]) # 65 kg, 163 cm
Khaled = np.array([20, 2])  # 92 kg, 168 cm
print("Hala: %.3f" % network.feedforward(Hala)) # 0.951 - F
print("Khaled: %.3f" % network.feedforward(Khaled)) # 0.039 - M
