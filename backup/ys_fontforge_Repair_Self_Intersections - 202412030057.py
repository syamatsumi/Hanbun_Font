#!fontforge --lang=py -script

import fontforge
import math

# �s�p�̃m�[�h���ς��֐��ł��B
# �A�C�f�A�o����������Ă��Ƃ�ChatGPT o1-preview�ɏ����Ė�����܂�܂ŁA
# �����ȂƂ���A�����Ɠ����Ă�̂��悭�킩��񂿂�B

# �����ڂɂ킩��Ȃ��قǏ����Ȏ��Ȍ����͐����s�p�������Ă��܂��B
# ���������ɂƂт����΃c�m�ɂȂ�܂����A
# ���������ɔ�яo���Ă��Ă���͂��яo���ċ���|�C���g�͉s�p�Ȃ̂ł��B
# �����ŁA�{�X�N���v�g�ł͉s�p������Ă���|�C���g����ӏ��Ɋ񂹏W�߂Ă��܂��܂��B
# ���Ƃ�glyph.removeOverlap()�ŏd�������|�C���g���폜����΂����̂ł����A
# �p�X�̌������������ȏ�Ԃ�glyph.removeOverlap()������
# ���̂܂܃O���t�����`���N�`���ɂȂ����Ⴄ�̂ŁA
# ������glyph.removeOverlap()�������Ă��܂���B
# �C�ӂ̃^�C�~���O�Ŏ��{����悤�ɂ��Ă��������B
# �ł���΂�������s�������オ��낵�����Ǝv���܂���B�i�L�́M �j

def ys_repair_Self_Insec(glyph, angle_threshold=2):
    import math
    angle_threshold_rad = math.radians(angle_threshold)
    two_pi = 2 * math.pi

    for contour in glyph.foreground:
        num_points = len(contour)
        # �I���N���[�u�|�C���g�̃C���f�b�N�X���擾
        on_curve_indices = [i for i, p in enumerate(contour) if p.on_curve]
        num_on_curve = len(on_curve_indices)
        i = 0
        while i < num_on_curve:  # �擾�����C���f�b�N�X����J��Ԃ�
            idx = on_curve_indices[i]
            current_point = contour[idx]

            # �p�x�̌v�Z
            prev_idx = on_curve_indices[i - 1]
            next_idx = on_curve_indices[(i + 1) % num_on_curve]
            # �����W�������Z�q�Ŕz��͈̔͊O�ɗ�����
            # �z��̐擪���Q�Ƃ���悤�Ɏd����ł���B
            prev_point = contour[prev_idx]
            next_point = contour[next_idx]

            # �x�N�g�����v�Z
            vector1 = (
                current_point.x - prev_point.x,
                current_point.y - prev_point.y,
            )
            vector2 = (
                next_point.x - current_point.x,
                next_point.y - current_point.y,
            )

            # �p�x���v�Z
            angle1 = math.atan2(vector1[1], vector1[0])
            angle2 = math.atan2(vector2[1], vector2[0])

            # ��̃x�N�g���̊Ԃ̊p�x�����v�Z
            angle_diff = (angle2 - angle1) % two_pi

            # �p�x����0����2�΂͈̔͂ɂȂ�悤�ɒ���
            if angle_diff < 0:
                angle_diff += two_pi

            # �p�x����0����2�΂͈̔͂ɐ��K��
            angle_diff = angle_diff % two_pi

            # �p�x��臒l�����܂���(2�� - 臒l)�𒴂���ꍇ��]��
            if angle_diff < angle_threshold_rad or (two_pi - angle_diff) < angle_threshold_rad:
                # ���̂���|�C���g�̘A�������o
                problem_oncurve_points = []
                problem_all_points = []  # �I���J�[�u�E�I�t�J�[�u���܂ޑS�Ẵ|�C���g
                start_idx = idx  # �J�n�C���f�b�N�X��ۑ�

                # ���̂���|�C���g�����W
                initial_i = i  # ���Z�O�����g�̊J�n�ʒu��ۑ�
                while True:
                    problem_oncurve_points.append(idx)
                    i += 1
                    if i >= num_on_curve:
                        break  # �֊s�̏I�[�ɓ��B

                    idx = on_curve_indices[i]
                    current_point = contour[idx]

                    # ���̊p�x���v�Z
                    prev_idx = on_curve_indices[i - 1]
                    next_idx = on_curve_indices[(i + 1) % num_on_curve]
                    prev_point = contour[prev_idx]
                    next_point = contour[next_idx]

                    vector1 = (
                        current_point.x - prev_point.x,
                        current_point.y - prev_point.y,
                    )
                    vector2 = (
                        next_point.x - current_point.x,
                        next_point.y - current_point.y,
                    )

                    angle1 = math.atan2(vector1[1], vector1[0])
                    angle2 = math.atan2(vector2[1], vector2[0])

                    angle_diff = (angle2 - angle1) % two_pi
                    if angle_diff < 0:
                        angle_diff += two_pi
                    angle_diff = angle_diff % two_pi

                    if angle_diff >= angle_threshold_rad and (two_pi - angle_diff) >= angle_threshold_rad:
                        # ���̂Ȃ��p�x�����ꂽ��I��
                        break

                end_idx = idx

                # �J�n�C���f�b�N�X����I���C���f�b�N�X�܂ł̃|�C���g�����W�i�I�t�J�[�u�|�C���g���܂ށj
                if start_idx <= end_idx:
                    indices_range = range(start_idx, end_idx + 1)
                else:
                    # �֊s�����Ă���ꍇ
                    indices_range = list(range(start_idx, num_points)) + list(range(0, end_idx + 1))

                for j in indices_range:
                    if j not in problem_all_points:
                        problem_all_points.append(j)

                # �n�_�ƏI�_�̃|�C���g���擾
                prev_oncurve_idx = on_curve_indices[(initial_i - 1) % num_on_curve]
                start_point = contour[prev_oncurve_idx]
                end_point = contour[end_idx]

                num_problems = len(problem_oncurve_points)

                if num_problems % 2 == 0:
                    # �����̏ꍇ�A���_�̕��ύ��W���v�Z
                    total_x = sum(contour[p_idx].x for p_idx in problem_oncurve_points)
                    total_y = sum(contour[p_idx].y for p_idx in problem_oncurve_points)
                    total_points = num_problems  # ���I���J�[�u�|�C���g��
                    avg_x = total_x / total_points
                    avg_y = total_y / total_points

                    # �n�_�ƏI�_�̍��W�͈͂��擾
                    min_x = min(start_point.x, end_point.x)
                    max_x = max(start_point.x, end_point.x)
                    min_y = min(start_point.y, end_point.y)
                    max_y = max(start_point.y, end_point.y)

                    # ���ύ��W���͈͓��ɂ��邩�̃`�F�b�N
                    x_in_range = min_x <= avg_x <= max_x
                    y_in_range = min_y <= avg_y <= max_y

                    if not x_in_range and not y_in_range:
                        # x����y���̗����Ŕ͈͊O�̏ꍇ�A�n�_�ƏI�_�̒��ԓ_���g�p
                        new_x = (start_point.x + end_point.x) / 2
                        new_y = (start_point.y + end_point.y) / 2
                    else:
                        # �����łȂ��ꍇ�A���ύ��W���g�p
                        new_x = avg_x
                        new_y = avg_y

                    # �n�_�ƏI�_�ɗאڂ���I�t�J�[�u�|�C���g���ړ��Ώۂ��珜�O
                    # �n�_�ɗאڂ���I�t�J�[�u�|�C���g
                    start_adjacent_idx = (start_idx + 1) % num_points
                    if not contour[start_adjacent_idx].on_curve and start_adjacent_idx in problem_all_points:
                        problem_all_points.remove(start_adjacent_idx)

                    # �I�_�ɗאڂ���I�t�J�[�u�|�C���g
                    end_adjacent_idx = (end_idx - 1) % num_points
                    if not contour[end_adjacent_idx].on_curve and end_adjacent_idx in problem_all_points:
                        problem_all_points.remove(end_adjacent_idx)

                else:
                    # ��̏ꍇ�A�n�_�ƏI�_�̒��ԓ_���g�p
                    new_x = (start_point.x + end_point.x) / 2
                    new_y = (start_point.y + end_point.y) / 2
                    # �I�t�J�[�u�|�C���g�͑S�Ĉړ��ΏۂɊ܂߂�

                # ���̂���S�Ẵ|�C���g�i�I�t�J�[�u�|�C���g�܂ށj��V�����ʒu�Ɉړ�
                for p_idx in problem_all_points:
                    contour[p_idx].x = new_x
                    contour[p_idx].y = new_y
            else:
                i += 1  # ���̃|�C���g�֐i��



if __name__ == "__main__":
    ys_rmSelfInsec(glyph, 2)