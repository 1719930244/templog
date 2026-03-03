#!/usr/bin/env python3
"""生成手术取消流程图 PDF - 带分组大框"""
import graphviz

dot = graphviz.Digraph(
    'surgery_cancel',
    format='pdf',
    engine='dot',
    graph_attr={
        'rankdir': 'TB',
        'splines': 'spline',
        'nodesep': '0.7',
        'ranksep': '0.5',
        'fontname': 'Noto Sans CJK SC',
        'fontsize': '20',
        'label': '手术取消流程\n',
        'labelloc': 't',
        'labeljust': 'c',
        'bgcolor': 'white',
        'pad': '0.5',
        'dpi': '150',
        'size': '14,18',
        'ratio': 'compress',
        'compound': 'true',
    },
    node_attr={
        'fontname': 'Noto Sans CJK SC',
        'fontsize': '11',
        'style': 'filled',
        'penwidth': '1.5',
        'margin': '0.15,0.08',
    },
    edge_attr={
        'color': '#555555',
        'penwidth': '1.2',
        'arrowsize': '0.8',
    }
)

# === 样式定义 ===
terminal = {
    'shape': 'ellipse', 'fillcolor': '#DAE8FC', 'color': '#6C8EBF',
    'fontsize': '14', 'fontcolor': '#333333', 'style': 'filled,bold',
}
process = {
    'shape': 'box', 'fillcolor': '#FFF2CC', 'color': '#D6B656',
    'fontsize': '12', 'style': 'filled,rounded',
}
nurse_s = {
    'shape': 'box', 'fillcolor': '#EAF4EA', 'color': '#82B366',
    'fontsize': '10', 'style': 'filled,rounded',
}
office_s = {
    'shape': 'box', 'fillcolor': '#F0EAF5', 'color': '#9673A6',
    'fontsize': '10', 'style': 'filled,rounded',
}
treat_s = {
    'shape': 'box', 'fillcolor': '#FDECEB', 'color': '#B85450',
    'fontsize': '10', 'style': 'filled,rounded',
}

# ========== 顶部节点 ==========
dot.node('start', '手术取消', **terminal)
dot.node('notify', '通知责任护士及相关人员', **process)

# ========== 责任护士 cluster ==========
with dot.subgraph(name='cluster_nurse') as c:
    c.attr(
        label='责任护士负责', fontname='Noto Sans CJK SC',
        fontsize='13', style='rounded,filled', color='#82B366',
        fillcolor='#D5E8D4', penwidth='2', labeljust='c',
    )
    c.node('n1', '1. 通知患者及家属手术取消\n   遵医嘱指导患者进食', **nurse_s)
    c.node('n2', '2. 填写相关护理记录', **nurse_s)
    c.node('n3', '3. 删除护理交接单', **nurse_s)
    c.node('n4', '4. 予患者心理护理', **nurse_s)
    c.edge('n1', 'n2')
    c.edge('n2', 'n3')
    c.edge('n3', 'n4')

# ========== 办公护士 cluster ==========
invis_node = {'shape': 'box', 'style': 'invis', 'width': '2', 'height': '0.4', 'fixedsize': 'true', 'label': ''}
invis_edge = {'style': 'invis'}

with dot.subgraph(name='cluster_office') as c:
    c.attr(
        label='办公护士负责', fontname='Noto Sans CJK SC',
        fontsize='13', style='rounded,filled', color='#9673A6',
        fillcolor='#E1D5E7', penwidth='2', labeljust='c',
    )
    c.node('o1', '1. 接收手术取消医嘱\n   并通知管床护士', **office_s)
    c.node('o2', '2. 退术前备药', **office_s)
    c.node('o3', '3. 擦黑板上的相应床号', **office_s)
    c.node('o_pad', **invis_node)
    c.edge('o1', 'o2')
    c.edge('o2', 'o3')
    c.edge('o3', 'o_pad', **invis_edge)

# ========== 治疗护士 cluster ==========
with dot.subgraph(name='cluster_treat') as c:
    c.attr(
        label='治疗护士负责', fontname='Noto Sans CJK SC',
        fontsize='13', style='rounded,filled', color='#B85450',
        fillcolor='#F8CECC', penwidth='2', labeljust='c',
    )
    c.node('t1', '与办公护士共同核对\n停止的术前用药', **treat_s)
    c.node('t_pad1', **invis_node)
    c.node('t_pad2', **invis_node)
    c.node('t_pad3', **invis_node)
    c.edge('t1', 't_pad1', **invis_edge)
    c.edge('t_pad1', 't_pad2', **invis_edge)
    c.edge('t_pad2', 't_pad3', **invis_edge)

# ========== 底部汇合 ==========
dot.node('verify', '双人核对电脑医嘱与\n执行单、贴药单、黑板等',
         shape='box', fillcolor='#FFF2CC', color='#D6B656',
         fontsize='12', style='filled,rounded,bold')
dot.node('end', '手术取消流程结束', **terminal)

# ========== 连线 ==========
dot.edge('start', 'notify')

# 从 notify 到三个 cluster（用 lhead 指向 cluster）
dot.edge('notify', 'n1', lhead='cluster_nurse')
dot.edge('notify', 'o1', lhead='cluster_office')
dot.edge('notify', 't1', lhead='cluster_treat')

# 从三个 cluster 底部汇合到 verify
dot.edge('n4', 'verify', ltail='cluster_nurse')
dot.edge('o_pad', 'verify', ltail='cluster_office', **invis_edge)
dot.edge('o3', 'verify')
dot.edge('t_pad3', 'verify', ltail='cluster_treat', **invis_edge)
dot.edge('t1', 'verify')

dot.edge('verify', 'end')

# ========== rank 对齐各行 ==========
for nodes in [
    ['n1', 'o1', 't1'],
    ['n2', 'o2', 't_pad1'],
    ['n3', 'o3', 't_pad2'],
    ['n4', 'o_pad', 't_pad3'],
]:
    with dot.subgraph() as s:
        s.attr(rank='same')
        for n in nodes:
            s.node(n)

# ========== 渲染 ==========
output_path = dot.render(
    filename='260226-surgery-cancel-flowchart',
    directory='/home/szw/github/templog',
    cleanup=True
)
print(f'PDF generated: {output_path}')
