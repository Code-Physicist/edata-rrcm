MyApp = {
  role_type_dict: { 0: "System Admin", 1: "Operator", 2: "Supervisor", 3: "Sup & Opt" },
  opn_type_badge_dict: {
    0: "<span class='badge border border-primary bg-primary-subtle text-primary'>System</span>",
    1: "<span class='badge border border-success bg-success-subtle text-success'>Data</span>",
    2: "<span class='badge border border-warning bg-warning-subtle text-warning'>Service</span>",
    3: "<span class='badge border border-info bg-info-subtle text-info'>Manufacturing</span>",
  },
  opn_type_dict: { 0: "System", 1: "Data", 2: "Service", 3: "Manufacturing" },
  status_dict: {
    0: "Idle",
    1: "Occupied",
    2: "Working",
    3: "Done",
    4: "End",
  },
  gender_dict: {
    1: "ชาย",
    2: "หญิง",
    3: "ไม่ระบุ"
  },
  priority_dict: {
    1: "<span class='badge border border-info bg-info-subtle text-info'>ปกติ</span>", 
    2: "<span class='badge border border-primary bg-primary-subtle text-primary'>เร่งด่วน</span>"
  },
  copy_vals: function (source, target, except_list = []) {
    for (let k in target) {
      if (except_list.includes(k)) continue;
      target[k] = source[k];
    }
  },
  get_file_ext(file_name) {
    // Split the filename by the dot character
    const parts = file_name.split('.');

    // Check if the filename has an extension
    if (parts.length > 1) {
        // Return the last part as the extension
        return parts.pop();
    } else {
        // No extension found
        return '';
    }
  },
  async get_users(opn_id) {
    const res = await axios.post("/api/get_users", {opn_id: opn_id});
    return res.data.data_list;
  },
  async get_users2(opn_id) {
    const res = await axios.post("/api/get_users2", {opn_id: opn_id});
    return res.data.data_list;
  },
  async get_med_operations() {
    const res = await axios.post("/api/get_med_operations");
    return res.data.data_list;
  },
  async get_nationalities() {
    const res = await axios.get("/api/get_nationalities");
    return res.data.data_list;
  },
  async get_prefixes() {
    const res = await axios.get("/api/get_prefixes");
    return res.data.data_list;
  },
  async get_rights() {
    const res = await axios.get("/api/get_rights");
    return res.data.data_list;
  },
  async get_provinces() {
    const res = await axios.get("/api/get_provinces");
    return res.data.data_list;
  },
  async get_amphurs(province_id) {
    const res = await axios.get(`/api/get_amphurs?province_id=${province_id}`);
    return res.data.data_list;
  },
  async get_tambons(amphur_id) {
    const res = await axios.get(`/api/get_tambons?amphur_id=${amphur_id}`);
    return res.data.data_list;
  },
  async get_sites() {
    const res = await axios.get("/api/get_sites");
    return res.data.data_list;
  },
  async get_operations() {
    const res = await axios.get("/api/get_operations");
    return res.data.data_list;
  },
  async get_routes() {
    const res = await axios.get("/api/get_routes");
    return res.data.data_list;
  },
  get_mime_type(base64_str) {
    const mime_type = base64_str.match(/^data:(image\/[a-zA-Z]+);base64,/);
    return mime_type ? mime_type[1] : null;
  },
  file_size_str(file_size) {
    const size = +file_size; // Ensure the file size is a number
    if (size < 1024) {
      return `${size} bytes`;
    } else if (size < 1048576) {
      return `${(size / 1024).toFixed(2)} KB`;
    } else if (size < 1073741824) {
      return `${(size / 1048576).toFixed(2)} MB`;
    } else {
      return `${(size / 1073741824).toFixed(2)} GB`;
    }
  },
  utc_time_str(local_time_str) {
    // Parse the local time string into a Date object
    const local_date = new Date(local_time_str);

    // Get the individual components in UTC
    const year = local_date.getUTCFullYear();
    const month = String(local_date.getUTCMonth() + 1).padStart(2, '0'); // Months are zero-based
    const day = String(local_date.getUTCDate()).padStart(2, '0');
    const hours = String(local_date.getUTCHours()).padStart(2, '0');
    const minutes = String(local_date.getUTCMinutes()).padStart(2, '0');
    const seconds = String(local_date.getUTCSeconds()).padStart(2, '0');

    // Format the components into a UTC time string
    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}Z`;
  },
  utc_time_str2(local_date) {
    // Get the individual components in UTC
    const year = local_date.getUTCFullYear();
    const month = String(local_date.getUTCMonth() + 1).padStart(2, '0'); // Months are zero-based
    const day = String(local_date.getUTCDate()).padStart(2, '0');
    const hours = String(local_date.getUTCHours()).padStart(2, '0');
    const minutes = String(local_date.getUTCMinutes()).padStart(2, '0');
    const seconds = String(local_date.getUTCSeconds()).padStart(2, '0');

    // Format the components into a UTC time string
    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}Z`;
  },
  local_time_str(local_date) {
    const year = local_date.getFullYear();
    const month = String(local_date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const day = String(local_date.getDate()).padStart(2, '0');
    const hours = String(local_date.getHours()).padStart(2, '0');
    const minutes = String(local_date.getMinutes()).padStart(2, '0');
    const seconds = String(local_date.getSeconds()).padStart(2, '0');

    // Format the components into a UTC time string
    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`;
  },
  local_time_str2(local_time_str, split=false, time_only=false) {
    const local_date = new Date(local_time_str);

    const year = local_date.getFullYear();
    const month = String(local_date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const day = String(local_date.getDate()).padStart(2, '0');
    const hours = String(local_date.getHours()).padStart(2, '0');
    const minutes = String(local_date.getMinutes()).padStart(2, '0');

    // Format the components into a UTC time string
    if(!split)
      if(time_only) return `${hours}:${minutes}`;
      else return `${day}/${month}/${year} ${hours}:${minutes}`;
    else
      return [`${day}/${month}/${year}`, `${hours}:${minutes}`]
  },
  iso_date_str(date_str)
  {
    //Convert "DD/MM/YYYY" to "YYYY-MM-DD"
    const [day, month, year] = date_str.split('/');
    return `${year}-${month}-${day}`;
  },
  user_date_str(date_str)
  {
    //Convert YYYY-MM-DD to "DD/MM/YYYY"
    const [year, month, day] = date_str.split('-');
    return `${day}/${month}/${year}`;
  }
};
