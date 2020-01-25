from app.models.questionnaire import Questionnaire


class CompleteForm:
    # 初始化 传入flag
    def __init__(self, flag):
        self.flag = flag
        self.questionnare = Questionnaire.objects.filter(questionnaireFlag=self.flag).first()

    def getCondition(self):
        if self.questionnare:
            data = {
                'questionnaireCondition': self.questionnare.questionnaireCondition,
                'questionnaireDeadline': self.questionnare.questionnaireDeadline,
                'questionnaireIsSecret': self.questionnare.questionnaireIsSecret,
                'questionnaireEquipmentControl': self.questionnare.questionnaireEquipmentControl,
            }
            return data
        return False

    def checkSecretKey(self, key):
        trueKey = self.questionnare.questionnaireSecretKey
        return trueKey == key

    def getProblems(self):
        return self.questionnare.questionnaireBasicData

    def subMitComplete(self, completeData, ip):
        # 返回0 :ip重复
        if ip in self.questionnare.questionnaireIP and self.questionnare.questionnaireIPControl:
            return 0
        # ip放入ip池里面
        self.questionnare.questionnaireIP.append(ip)
        # 导入填报数据
        self.questionnare.questionnaireCompleteResult.append(completeData)
        self.questionnare.save()
        return 1
