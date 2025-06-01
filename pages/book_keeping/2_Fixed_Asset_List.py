import streamlit as st
from streamlit_modal import Modal
import pandas as pd
import datetime
from app.types.fixed_asset import  FixedAsset
from services.fixed_assets import entry, list, bulk_update, bulk_delete, fixed_asset_options, calculate_straight_line_method
from settings import logger
from constants import options
"""
### 固定資産台帳
"""
st.write("会計期間: %s - %s" % (st.session_state['fiscal_start_date'].strftime("%Y-%m-%d"), st.session_state['fiscal_end_date'].strftime("%Y-%m-%d")))

@st.cache_data
def fixed_asset_options_cached():
    return fixed_asset_options()

fixed_assets = []
depreciating_plan = []

(fiscal_end_year, fiscal_end_month) =  (st.session_state['fiscal_end_date'].year, st.session_state['fiscal_end_date'].month)

depreciating_expense = [0, 0, 0, 0, 0]
fixed_asset_amount_total = 0
fixed_asset_depreciation_expense_total_at_last_fiscal_year_total = 0
depreciating_expense_0_total = 0
depreciating_expense_1_total = 0
depreciating_expense_2_total = 0
depreciating_expense_3_total = 0
depreciating_expense_4_total = 0
depreciating_expense_remain_total = 0

for fixed_asset in list():
    depreciation_data = calculate_straight_line_method(
        obtained_at=fixed_asset.obtained_at,
        depreciating_years=fixed_asset.depreciating_years,
        amount=fixed_asset.amount,
        depreciation_expense_total_at_last_fiscal_year=fixed_asset.depreciation_expense_total_at_last_fiscal_year
    )

    depreciation_expenses_by_fiscal_year = depreciation_data["depreciation_expenses_by_fiscal_year"]

    fixed_assets.append({
        "edit": False,
        "資産名称": fixed_asset.name,
        "種類": fixed_asset.item,
        "着工日": fixed_asset.launched_at,
        "取得日": fixed_asset.obtained_at,
        "取得形態": fixed_asset.obtained_type,
        "金額(税抜き)": fixed_asset.amount,
        "構造又は用途": fixed_asset.structure_or_use,
        "細目": fixed_asset.details,
        "耐用年数": fixed_asset.depreciating_years,
        "償却終了年月": depreciation_data["depreciation_end_date"].strftime('%Y-%m'),
        "減価償却費累計額(前期末)": fixed_asset.depreciation_expense_total_at_last_fiscal_year,
        "当期償却予定額": depreciation_expenses_by_fiscal_year[st.session_state['fiscal_term']] if st.session_state['fiscal_term'] in depreciation_expenses_by_fiscal_year else 0,
        "設置場所": fixed_asset.location,
        "備考": fixed_asset.remark,
        "id": fixed_asset.id,
    })

    depreciating_expense[0] = depreciation_expenses_by_fiscal_year[st.session_state['fiscal_term']] if st.session_state['fiscal_term'] in depreciation_expenses_by_fiscal_year else 0
    depreciating_expense[1] = depreciation_expenses_by_fiscal_year[f'{fiscal_end_year + 1}年{fiscal_end_month:02}月期'] if f'{fiscal_end_year + 1}年{fiscal_end_month:02}月期' in depreciation_expenses_by_fiscal_year else 0
    depreciating_expense[2] = depreciation_expenses_by_fiscal_year[f'{fiscal_end_year + 2}年{fiscal_end_month:02}月期'] if f'{fiscal_end_year + 2}年{fiscal_end_month:02}月期' in depreciation_expenses_by_fiscal_year else 0
    depreciating_expense[3] = depreciation_expenses_by_fiscal_year[f'{fiscal_end_year + 3}年{fiscal_end_month:02}月期'] if f'{fiscal_end_year + 3}年{fiscal_end_month:02}月期' in depreciation_expenses_by_fiscal_year else 0
    depreciating_expense[4] = depreciation_expenses_by_fiscal_year[f'{fiscal_end_year + 4}年{fiscal_end_month:02}月期'] if f'{fiscal_end_year + 4}年{fiscal_end_month:02}月期' in depreciation_expenses_by_fiscal_year else 0
    depreciating_expense_remain = fixed_asset.amount - fixed_asset.depreciation_expense_total_at_last_fiscal_year - sum(depreciating_expense)

    # 端数調整
    if depreciating_expense_remain != 0 and depreciating_expense[4] == 0:
        for i in reversed(range(len(depreciating_expense))):
            if depreciating_expense[i] > 0:
                depreciating_expense[i] += depreciating_expense_remain
                depreciating_expense_remain = 0
                break

    depreciating_plan.append({
        "資産名称": fixed_asset.name,
        "種類": fixed_asset.item,
        "耐用年数": fixed_asset.depreciating_years,
        "取得年月": fixed_asset.obtained_at.strftime('%Y-%m'),
        "償却終了年月": depreciation_data["depreciation_end_date"].strftime('%Y-%m'),
        "減価償却費累計額(前期末)": fixed_asset.depreciation_expense_total_at_last_fiscal_year,
        st.session_state['fiscal_term']: depreciating_expense[0],
        f'{fiscal_end_year + 1}年{fiscal_end_month:02}月期': depreciating_expense[1],
        f'{fiscal_end_year + 2}年{fiscal_end_month:02}月期': depreciating_expense[2],
        f'{fiscal_end_year + 3}年{fiscal_end_month:02}月期': depreciating_expense[3],
        f'{fiscal_end_year + 4}年{fiscal_end_month:02}月期': depreciating_expense[4],
        f'{fiscal_end_year + 5}年{fiscal_end_month:02}月期〜': depreciating_expense_remain,
        "金額(税抜き)": fixed_asset.amount,
    })

    fixed_asset_amount_total += fixed_asset.amount
    fixed_asset_depreciation_expense_total_at_last_fiscal_year_total += fixed_asset.depreciation_expense_total_at_last_fiscal_year
    depreciating_expense_0_total += depreciating_expense[0]
    depreciating_expense_1_total += depreciating_expense[1]
    depreciating_expense_2_total += depreciating_expense[2]
    depreciating_expense_3_total += depreciating_expense[3]
    depreciating_expense_4_total += depreciating_expense[4]
    depreciating_expense_remain_total += depreciating_expense_remain

summary_depreciating_plan = [{
    "前期末累計": fixed_asset_depreciation_expense_total_at_last_fiscal_year_total,
    st.session_state['fiscal_term']: depreciating_expense_0_total,
    f'{fiscal_end_year + 1}年{fiscal_end_month:02}月期': depreciating_expense_1_total,
    f'{fiscal_end_year + 2}年{fiscal_end_month:02}月期': depreciating_expense_2_total,
    f'{fiscal_end_year + 3}年{fiscal_end_month:02}月期': depreciating_expense_3_total,
    f'{fiscal_end_year + 4}年{fiscal_end_month:02}月期': depreciating_expense_4_total,
    f'{fiscal_end_year + 5}年{fiscal_end_month:02}月期〜': depreciating_expense_remain_total,
    "金額(税抜き)": fixed_asset_amount_total,
}]

df_fixed_assets = pd.DataFrame(fixed_assets)

# 固定資産登録モーダル
fixed_asset_modal = Modal(
    ":pencil: 固定資産を登録",
    key="entry-asset-modal",
    padding=20,
    max_width=800,
)

if fixed_asset_modal.is_open():
    with fixed_asset_modal.container():

        name = st.text_input(label="資産名称", key="asset-name")
        launched_at = st.date_input("着工日", datetime.date.today(), key="asset-launched-at")
        obtained_at = st.date_input("取得日", datetime.date.today(), key="asset-obtained-at")
        obtained_type = st.selectbox(label="取得形態", options=options.fixed_asset_obtained_types, key="obtain-types")
        item = st.selectbox(label="種類", options=fixed_asset_options(), key="asset-options")
        amount = st.text_input("金額(税抜き)", key="amount")
        structure_or_use = st.text_input("構造又は用途", key="structure-or-use")
        details = st.text_input("細目", key="details")
        depreciating_years = st.text_input("耐用年数", key="depreciating-years")
        location = st.text_input("設置場所", key="location")
        remark = st.text_area("備考", height=80, max_chars=255, key="remark")

        st.write('種類、構造又は用途、細目については[減価償却資産の耐用年数等に関する省令](https://laws.e-gov.go.jp/law/340M50000040015/) 別表第一をもとに入力')

        if st.button("新規作成", type="primary", key="entry-asset-button"):
            try:
                entry(fixed_asset=FixedAsset(
                    name=name,
                    launched_at=launched_at,
                    obtained_at=obtained_at,
                    obtained_type=obtained_type,
                    item=item,
                    amount=amount,
                    structure_or_use=structure_or_use,
                    details=details,
                    depreciating_years=depreciating_years,
                    location=location,
                    remark=remark,
                ))
                fixed_asset_modal.close()
                st.toast('固定資産を登録しました')
            except Exception as e:
                logger.error(e)
                st.toast(e)

# 固定資産登録モーダル
fixed_asset_entry_journals_modal = Modal(
    ":pencil: 仕訳データ作成",
    key="entry-journals-modal",
    padding=20,
    max_width=800,
)

if fixed_asset_entry_journals_modal.is_open():
    with fixed_asset_entry_journals_modal.container():
        obtained_at_from = st.session_state['fiscal_start_date'].strftime("%Y-%m-%d")
        obtained_at_to = st.session_state['fiscal_end_date'].strftime("%Y-%m-%d")

        df_fixed_assset_obtained_this_fiscal_year = df_fixed_assets.query(f"('{obtained_at_from}' <= 取得日 <= '{obtained_at_to}') & 取得形態 in ['購入', 'リース']")
        df_fixed_assset_obtained_until_this_fiscal_year = df_fixed_assets.query(f"(取得日 <= '{obtained_at_to}') & 取得形態 in ['購入', 'リース']")

        st.write('##### 今期取得の固定資産')
        st.dataframe(
            df_fixed_assset_obtained_this_fiscal_year[["種類", "取得形態", "資産名称", "取得日", "金額(税抜き)"]],
            column_config={
                "取得日": st.column_config.DateColumn(
                    "取得日",
                ),
            },
            hide_index=True
        )
        st.write(f'今期取得の固定資産 合計額 {df_fixed_assset_obtained_this_fiscal_year["金額(税抜き)"].sum():,}円')
        st.caption(f'(注1) 相手方勘定を「建設仮勘定」として仕訳を作成します。')

        st.write('##### 当期償却額')
        st.dataframe(
            df_fixed_assset_obtained_until_this_fiscal_year[["種類", "取得形態", "資産名称", "取得日", "金額(税抜き)"]],
            column_config={
                "取得日": st.column_config.DateColumn(
                    "取得日",
                ),
            },
            hide_index=True
        )
        st.write(f'当期償却予定 合計額 {df_fixed_assset_obtained_until_this_fiscal_year["当期償却予定額"].sum():,}円')
        st.caption(f'(注2) 「販売費及び一般管理費 / 減価償却費累計額」の仕訳を作成します。')

        if st.button("仕訳データ作成", type="primary", key="confirm-entry-journals-button"):
            # reentry_obtaining_fixed_asssets_journals(df_fixed_assset_obtained_this_fiscal_year[["種類", "取得形態", "資産名称", "取得日", "金額(税抜き)"]])
            # reentry_depreciation_expense_journals(df_fixed_assset_obtained_until_this_fiscal_year[["種類", "取得形態", "資産名称", "取得日", "金額(税抜き)"]])
            fixed_asset_entry_journals_modal.close()

        st.caption(f'※ 合計残高試算表等で確認して差額がある場合は訂正し、再度「仕訳データ作成」を行い今期の仕訳を洗い替えします。')

fixed_assets_details_tab, depreciating_plan_tab = st.tabs(["一覧", "償却計画"])

with fixed_assets_details_tab:

    fixed_assets_edited = st.data_editor(
        df_fixed_assets,
        width=800,
        height=600,
        column_config={
            "着工日": st.column_config.DateColumn(
                "着工日",
            ),
            "取得日": st.column_config.DateColumn(
                "取得日",
            ),
            "取得形態": st.column_config.SelectboxColumn(
                "取得形態",
                options=options.fixed_asset_obtained_types,
            ),
            "種類": st.column_config.SelectboxColumn(
                "種類",
                options=fixed_asset_options_cached(),
            ),
        },
        disabled=["償却終了年月", "当期償却予定額", "id"],
        hide_index=True,
    )

    col01, col02, col03 = st.columns(3)

    with col01:
        if st.button("固定資産を登録", type="secondary", use_container_width=True, key="open-asset-button"):
            fixed_asset_modal.open()

    with col02:
        if st.button("チェックしたものを更新", type="secondary", use_container_width=True, key="update-asset-button"):
            res = bulk_update(fixed_assets_edited.query('edit == True'))
            st.rerun()

    with col03:
        if st.button("チェックしたものを削除", type="primary", use_container_width=True, key="delete-asset-button"):
            bulk_delete(fixed_assets_edited.query('edit == True'))
            st.rerun()

    if st.button("仕訳データ作成", type="secondary", use_container_width=True, key="entry-journals-button"):
        fixed_asset_entry_journals_modal.open()

with depreciating_plan_tab:
    st.dataframe(
        pd.DataFrame(depreciating_plan),
        width=800,
        height=600,
        hide_index=True,
    )

    st.dataframe(
        pd.DataFrame(summary_depreciating_plan),
        width=800,
        hide_index=True,
    )

# style
st.markdown("""
    <style>
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""", unsafe_allow_html=True)
