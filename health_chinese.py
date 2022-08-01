##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2022 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2022 GNU Solidario <health@gnusolidario.org>
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from trytond.model import ModelView, ModelSQL, fields
from trytond.rpc import RPC
from trytond.pyson import Eval, Not, Bool, Equal, Or
import hashlib
import json


__all__ = ['Party']

family_names_one_char=[
    '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈',
    '韩', '杨', '朱', '秦', '尤', '许', '何', '吕', '施', '张', '孔', '曹', '严', '华', 
    '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏', 
    '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方',
    '俞', '任', '袁', '柳', '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', 
    '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常', '乐', '于', '时', '傅', 
    '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', 
    '萧', '尹', '姚', '邵', '湛', '汪', '祁', '与', '禹', '狄', '米', '贝', '明', '臧', 
    '计', '伏', '成', '戴', '谈', '宋', '茅', '庞', '熊', '纪', '舒', '屈', '项', '祝', 
    '董', '粱', '杜', '阮', '蓝', '闵', '席', '季', '麻', '强', '贾', '路', '娄', '危', 
    '刘', '童', '颜', '郭', '梅', '盛', '林', '刁', '钟', '徐', '邱', '骆', '高', '夏', 
    '蔡', '田', '樊', '邹', '凌', '霍', '虞', '万', '支', '柯', '昝', '管', '卢', '莫', 
    '经', '房', '裘', '缪', '干', '解', '应', '宗', '丁', '宣', '贲', '邓', '郁', '单', 
    '杭', '洪', '包', '诸', '左', '石', '崔', '吉', '钮', '龚', '程', '嵇', '邢', '滑', 
    '裴', '陆', '荣', '翁', '荀', '羊', '於', '惠', '甄', '麴', '家', '封', '芮', '羿', 
    '储', '靳', '汲', '邴', '糜', '松', '井', '段', '富', '巫', '乌', '焦', '巴', '弓', 
    '牧', '隗', '山', '谷', '车', '侯', '宓', '蓬', '全', '郗', '班', '仰', '秋', '仲', 
    '伊', '宫', '宁', '仇', '栾', '暴', '甘', '钭', '厉', '戎', '祖', '武', '符', '刘', 
    '景', '詹', '束', '龙', '叶', '幸', '司', '韶', '郜', '黎', '蓟', '薄', '印', '宿', 
    '白', '怀', '蒲', '邰', '从', '鄂', '索', '咸', '籍', '赖', '卓', '蔺', '屠', '蒙', 
    '冉', '宰', '郦', '雍', '舄', '璩', '桑', '桂', '濮', '牛', '寿', '通', '边', '扈', 
    '燕', '冀', '郏', '浦', '尚', '农', '温', '别', '庄', '晏', '柴', '瞿', '阎', '充', 
    '慕', '连', '茹', '有', '宦', '艾', '鱼', '容', '向', '古', '易', '慎', '戈', '廖', 
    '庾', '终', '暨', '居', '衡', '步', '都', '耿', '满', '弘', '匡', '国', '文', '寇', 
    '广', '禄', '阙', '东', '殴', '殳', '沃', '利', '蔚', '越', '夔', '隆', '师', '巩', 
    '厍', '聂', '晁', '勾', '敖', '融', '冷', '訾', '辛', '阚', '那', '简', '饶', '空', 
    '曾', '毋', '沙', '乜', '养', '鞠', '须', '丰', '巢', '关', '蒯', '相', '查', '後', 
    '荆', '红', '游', '竺', '权', '逯', '盖', '益', '桓', '公', '晋', '楚', '闫', '法', 
    '汝', '鄢', '涂', '钦', '岳', '帅', '缑', '亢', '况', '后', '有', '琴', '商', '牟', 
    '佘', '佴', '伯', '赏', '墨', '哈', '谯', '笪', '年', '爱', '阳', '佟', '言', '福', 
    '百', '家', '姓', '终', '仉', '督', '归', '海']

family_names_two_chars=[
    '万俟', '司马', '上官', '欧阳', '夏侯', '诸葛', '闻人', '东方', '赫连', '皇甫', '尉迟',
    '公羊', '澹台', '公冶', '宗政', '濮阳', '淳于', '单于', '太叔', '申屠', '公孙', '仲孙',
    '轩辕', '令狐', '钟离', '宇文', '长孙', '慕容', '鲜于', '闾丘', '司徒', '司空', '亓官',
    '司寇', '子车', '颛孙', '端木', '巫马', '公西', '漆雕', '乐正', '壤驷', '公良', '拓跋', 
    '夹谷', '宰父', '谷梁', '段干', '百里', '东郭', '南门', '呼延', '羊舌', '微生', '梁丘', 
    '左丘', '东门', '西门', '南宫', '第五']

class Party(ModelSQL, ModelView):
    __name__ = 'party.party'

    # cn_full_name = fields.Char('Chinese full name')

    @classmethod
    def create(cls, vlist):
        vlist = [x.copy() for x in vlist]
        print('beg1---------------------------------')
        print(vlist)
        print('end1---------------------------------')
        for values in vlist:
            if (values['name'] != '') and (values['lastname'] == ''):
                one_char = values['name'][0:1]
                two_chars = values['name'][0:2]
                if (two_chars in family_names_two_chars):
                    family_name = values['name'][0:2]
                    given_name = values['name'][2:]
                elif (one_char in family_names_one_char):
                    family_name = values['name'][0:1]
                    given_name = values['name'][1:]
                else:
                    family_name = ''
                    given_name = values['name']

                values['name'] = given_name
                values['lastname'] = family_name

        return super(Party, cls).create(vlist)

    # @classmethod
    # def search_rec_name(cls, name, clause):
    #     """ Search for the name, lastname, PUID, any alternative IDs,
    #         and any family and / or given name from the person_names
    #     """
    #     if clause[1].startswith('!') or clause[1].startswith('not '):
    #         bool_op = 'AND'
    #     else:
    #         bool_op = 'OR'
    #     return [bool_op,
    #             ('ref',) + tuple(clause[1:]),
    #             ('alternative_ids.code',) + tuple(clause[1:]),
    #             ('federation_account',) + tuple(clause[1:]),
    #             ('contact_mechanisms.value',) + tuple(clause[1:]),
    #             ('person_names.family',) + tuple(clause[1:]),
    #             ('person_names.given',) + tuple(clause[1:]),
    #             ('name',) + tuple(clause[1:]),
    #             ('lastname',) + tuple(clause[1:]),
    #             ]

