# --------------------------------------------------
# 處理 post
def post_json(raw_input):
    raw_input['renter.renter_role'] = raw_input["renter"]["renter_role"]
    raw_input['renter.renter_fname'] = raw_input["renter"]["renter_fname"]
    raw_input['renter.renter_title'] = raw_input["renter"]["renter_title"]
    raw_input.pop("renter")
    raw_dict = {k:v for k,v in raw_input.items() if v is not None}
    dictlist = []
    for key, value in raw_dict.items():
        temp = {key: value}
        dictlist.append(temp)
    return dictlist